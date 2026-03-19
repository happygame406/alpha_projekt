# Запуск проекта
1. Убедитесь, что у вас есть доступ к базе данных PostgreSQL
2. Зайдите в файл `database.py` и замените DATABASE_URL на `postgresql+asyncpg://user:password@host:port/db_name`, где `user` - это имя пользователя, `password` - пароль пользователя БД, `host` - хост, где находится БД (например, localhost), `port` - порт, `db_name` - название БД. Далее заходим в файл `alembic.ini` и заменяем `sqlalchemy_url` на `postgresql+psycopg://user:password@host:port/db_name`
3. Установите пакеты командой `pip install requirements.txt`
4. Примените миграцию, которая уже создана командой `alembic upgrade head`
5. Далее используйте команду `uvicorn main:app --reload` в той же папке, где находится файл `main.py`
6. Если все сделано верно, то проект должен открыться в `http://127.0.0.1:8000/`

# Модели данных
## Item
```id - int (первичный ключ)
user_id - int (связь с пользователем, вторичный ключ модели User)
title - str (название товара)
desciption - str (описание товара)
```

## User
```id - int (первичный ключ)
username - str (никнейм пользователя
is_active - bool (активен ли пользователь или нет)
```

К одному User можно связать много Item, но не наоборот, так что связь User : Item является 1 : М
