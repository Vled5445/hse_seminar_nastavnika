import os
import pandas as pd
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Определение модели данных Pydantic
class RecordBase(BaseModel):
    timestep: str
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float

class RecordCreate(RecordBase):
    pass

class Record(RecordBase):
    id: str

# Путь к файлу данных
DATA_FILE = "data.csv"
BACKUP_FILE = "data_backup.csv"

def load_data() -> pd.DataFrame:
    """Загрузка данных из CSV файла"""
    if not os.path.exists(DATA_FILE):
        # Создаем пустой DataFrame, если файл не существует
        df = pd.DataFrame(columns=[
            'id', 'timestep', 
            'consumption_eur', 'consumption_sib',
            'price_eur', 'price_sib'
        ])
        df.to_csv(DATA_FILE, index=False)
        return df
    
    df = pd.read_csv(DATA_FILE)
    
    # Преобразование старых данных (без id)
    if 'id' not in df.columns:
        # Создаем id для существующих записей
        df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_csv(DATA_FILE, index=False)
    
    # Проверка данных
    required_columns = [
        'timestep', 'consumption_eur', 'consumption_sib', 
        'price_eur', 'price_sib'
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column in CSV: {col}")
    
    return df

def save_data(df: pd.DataFrame):
    """Сохранение данных в CSV файл с созданием резервной копии"""
    # Создаем резервную копию
    if os.path.exists(DATA_FILE):
        os.replace(DATA_FILE, BACKUP_FILE)
    
    # Сохраняем новые данные
    df.to_csv(DATA_FILE, index=False)

@app.get("/records", response_model=List[Record])
def get_records():
    """Получение всех записей"""
    try:
        df = load_data()
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/records", response_model=Record)
def create_record(record: RecordCreate):
    """Добавление новой записи"""
    try:
        df = load_data()
        
        # Создаем новую запись с уникальным id
        new_id = str(uuid.uuid4())
        new_record = record.dict()
        new_record['id'] = new_id
        
        # Добавляем в DataFrame
        new_df = pd.concat([
            df, 
            pd.DataFrame([new_record])
        ], ignore_index=True)
        
        # Сохраняем данные
        save_data(new_df)
        return new_record
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/records/{record_id}")
def delete_record(record_id: str):
    """Удаление записи по ID"""
    try:
        df = load_data()
        
        # Проверка существования записи
        if record_id not in df['id'].values:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Удаление записи
        new_df = df[df['id'] != record_id]
        
        # Сохраняем данные
        save_data(new_df)
        return {"message": "Record deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Сервис для отдачи файла данных (для дебага)
@app.get("/download_data")
async def download_data():
    return FileResponse(DATA_FILE)
