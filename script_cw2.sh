echo "Введите название файла:"
read file_name
if [ -f "$file_name" ]; then 
	echo "file is exists"
else
	echo "File is not exists"
fi
