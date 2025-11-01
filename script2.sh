echo "1. Текущее значение PATH:"
echo "   $PATH"

new_dir="aab"
echo "2. Добавляем директорию '$new_dir' в PATH"
export PATH="$PATH/$new_dir"
echo "   Новое значение PATH:"
echo "   $PATH"

