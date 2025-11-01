for item in *; do
    if [ -f "$item" ]; then
        echo "   Файл: $item"
    elif [ -d "$item" ]; then
        echo "   Каталог: $item"
    elif [ -L "$item" ]; then
        echo "   Ссылка: $item"
    else
        echo "   Другой тип: $item"
    fi
done

echo

if [ $# -eq 0 ]; then
    echo "2. Ошибка: Укажите имя файла как аргумент скрипта"
    echo "   Использование: $0 <имя_файла>"
else
    filename=$1
    if [ -e "$filename" ]; then
        echo "2. Файл '$filename' существует"
    else
        echo "2. Файл '$filename' не существует"
    fi
fi

echo

echo "3. Информация о файлах (имя и права доступа):"
for file in *; do
    if [ -e "$file" ]; then
        permissions=$(ls -ld "$file" | cut -d' ' -f1)
        echo "   $file: $permissions"
    fi
done
