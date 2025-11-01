greet() {
    if [ $# -eq 0 ]; then
        echo "Ошибка: Функция greet требует аргумент"
        return 1
    fi
    echo "Hello, $1"
}

sum_numbers() {
    if [ $# -ne 2 ]; then
        echo "Ошибка: Функция sum_numbers требует два аргумента"
        return 1
    fi
    
    if ! [[ $1 =~ ^-?[0-9]+$ ]] || ! [[ $2 =~ ^-?[0-9]+$ ]]; then
        echo "Ошибка: Оба аргумента должны быть числами"
        return 1
    fi
    
    local sum=$(( $1 + $2 ))
    echo $sum  # Возвращаем результат
}

# Демонстрация работы функций
echo "1. Демонстрация функции greet:"
greet "World"
greet "Bash"
greet "User"

echo

echo "2. Демонстрация функции sum_numbers:"
result1=$(sum_numbers 13 29)
echo "   Сумма 13 и 29: $result1"

result2=$(sum_numbers -1 -5)
echo "   Сумма -1 и -5: $result2"

result3=$(sum_numbers -10 110)
echo "Сумма -10 и 110: $result3"
