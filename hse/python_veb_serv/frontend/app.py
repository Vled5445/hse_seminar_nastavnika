import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
from datetime import datetime

# Конфигурация страницы
st.set_page_config(
    page_title="Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

API_URL = "http://localhost:8000"  

def fetch_data():
    """Загрузка данных с backend"""
    try:
        response = requests.get(f"{API_URL}/records")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def validate_timestep(value: str):
    """Валидация формата временной метки"""
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def display_dashboard():
    """Отображение основного интерфейса"""
    st.title("Energy Consumption Dashboard")

    data = fetch_data()
    df = pd.DataFrame(data)

    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Power Consumption")
            fig = px.line(
                df,
                x='timestep',
                y=['consumption_eur', 'consumption_sib'],
                labels={"value": "MW", "variable": "Region"},
                title="European vs Siberian Power Consumption"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Electricity Prices")
            fig = px.line(
                df,
                x='timestep',
                y=['price_eur', 'price_sib'],
                labels={"value": "RUB/MWh", "variable": "Region"},
                title="European vs Siberian Electricity Prices"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available. Please add new records.")

    st.subheader("Data")
    if not df.empty:
        df_display = df.drop(columns=['price_sib', 'consumption_sib'])
        st.dataframe(df_display)
    else:
        st.info("No data to display")

    st.subheader("Add New Record")
    with st.form("add_record_form"):
        timestep = st.text_input(
            "Timestamp (YYYY-MM-DD HH:MM)", 
            placeholder="2026-03-01 01:00"
        )
        consumption_eur = st.number_input("Consumption EUR (MW)", min_value=0.0)
        consumption_sib = st.number_input("Consumption SIB (MW)", min_value=0.0)
        price_eur = st.number_input("Price EUR (RUB/MWh)", min_value=0.0)
        price_sib = st.number_input("Price SIB (RUB/MWh)", min_value=0.0)
        
        submitted = st.form_submit_button("Add Record")
        
        if submitted:
            if not validate_timestep(timestep):
                st.error("Invalid timestamp format! Use YYYY-MM-DD HH:MM")
            else:
                new_record = {
                    "timestep": timestep,
                    "consumption_eur": consumption_eur,
                    "consumption_sib": consumption_sib,
                    "price_eur": price_eur,
                    "price_sib": price_sib
                }
                
                try:
                    response = requests.post(
                        f"{API_URL}/records", 
                        json=new_record
                    )
                    if response.status_code == 200:
                        st.success("✅ Record added successfully!")
                        time.sleep(1)
                        st.experimental_rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except:
                    st.error("API connection error")

    st.subheader("Delete Record")
    record_id = st.text_input("Enter Record ID to delete")
    if st.button("Delete"):
        if not record_id:
            st.warning("Please enter a record ID")
        else:
            try:
                response = requests.delete(f"{API_URL}/records/{record_id}")
                if response.status_code == 200:
                    st.success("Record deleted successfully!")
                    time.sleep(1)
                    st.experimental_rerun()
                elif response.status_code == 404:
                    st.error("Record not found")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except:
                st.error("API connection error")

if __name__ == "__main__":
    display_dashboard()
