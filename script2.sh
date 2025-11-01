echo "Текущее значение PATH:"
echo "   $PATH"

new_dir="aab"
echo "2. Добавление директории '$new_dir' в PATH"
export PATH="$PATH:$new_dir"
echo "Новое значение PATH:"
echo "$PATH"

echo "Объяснение:"
echo "Изменения PATH через терминал временные - они действуют только"
echo "в текущей сессии терминала."
echo
echo "export PATH=\"\$PATH:$new_dir\""
echo
echo "echo 'export PATH=\"\\\$PATH:$new_dir\"' >> ~/.bashrc"
echo "source ~/.bashrc"
