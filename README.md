## Инструкция по запуску :
1. Находясь в папке с проектом создайте .env файл со следующим содержанием:
```bash
DB_NAME=ваше имя базы данных
DB_USER=ваш логин к базе данных
DB_PASSWORD=ваш пароль к базе данных
DB_PORT=ваш порт для базы данных
SECRET_KEY=ваш произвольный секретный ключ 
```
Пример:
```bash
DB_NAME=articles
DB_USER=user
DB_PASSWORD=passwd
DB_PORT=5454
SECRET_KEY=asdik3244klkasdlk1_)sdaq
```

2) Соберите и запустите контейнеры:
```
docker-compose up --build
```

Приложение будет достпуно по адресу http://127.0.0.1:8080
