# Устанавливаем текущую дату и время
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Путь к каталогу для сохранения резервных копий на хостовой машине
HOST_BACKUP_DIR="/path/to/host/backup/directory"

# Название базы данных PostgreSQL
DB_NAME="postgres"

# Название файла для резервной копии
BACKUP_FILE="$HOST_BACKUP_DIR/$DB_NAME-$TIMESTAMP.backup"

# Выполняем резервное копирование с помощью pg_dump внутри контейнера
docker-compose exec -T pgdb pg_dump -U postgres -Fc $DB_NAME > $BACKUP_FILE

# Проверяем успешность выполнения резервного копирования
if [ $? -eq 0 ]; then
    echo "Резервное копирование успешно завершено: $BACKUP_FILE"
else
    echo "Ошибка при выполнении резервного копирования"
fi