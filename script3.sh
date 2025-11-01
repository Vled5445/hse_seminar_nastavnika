read -p "Введите число: " number

echo "1. Проверка числа:"
if [ "$number" -gt 0 ] 2>/dev/null; then
    echo "Число $number положительное"
elif [ "$number" -lt 0 ] 2>/dev/null; then
    echo "Число $number отрицательное"
elif [ "$number" -eq 0 ] 2>/dev/null; then
    echo "Число равно нулю"
else
    echo "Ошибка: '$number' не является числом"
    exit 1
fi

if [ "$number" -gt 0 ] 2>/dev/null; then
    echo "Подсчет от 1 до $number:"
    counter=1
    while [ $counter -le $number ]; do
        echo "   $counter"
        ((counter++))
    done
else
    echo "2. Подсчет не выполнен (число не положительное)"
fi
