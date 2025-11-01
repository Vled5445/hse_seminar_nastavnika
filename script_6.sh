echo "Подсчет строк и запись в output.txt:"
wc -l < input.txt > output.txt
echo "Результат записан в output.txt:"
cat output.txt

echo "Перенаправление ошибок в error.log:"
ls no_name_a.txt 2> error.log
echo "Ошибки записаны в error.log:"
cat error.log

