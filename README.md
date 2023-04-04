## Инструкция по запуску:
1. Находясь в папке с проектом создайте .env файл со следующим содержанием:
```bash
DB_NAME=ваше имя базы данных
DB_USER=ваш логин к базе данных
DB_PASSWORD=ваш пароль к базе данных
DB_PORT=ваш порт для базы данных (должен быть свободен)
SECRET_KEY=ваш произвольный секретный ключ 
EMAIL_USER=ваш адрес эл. почты, откуда будут отправляться письма
EMAIL_PASSWORD=пароль от эл. почты
EMAIL_HOST=сервер отправителя писем (по умолчанию smtp.yandex.com)
```
Пример:
```bash
DB_NAME=articles
DB_USER=user
DB_PASSWORD=passwd
DB_PORT=5454
SECRET_KEY=asdik3244klkasdlk1_)sdaq
EMAIL_USER=myauthmanager@ya.ru
EMAIL_PASSWORD=mdskmfkmerw32kklas
```

2) Соберите и запустите контейнеры:
```
docker-compose up --build
```

Приложение будет достпуно по адресу http://127.0.0.1:8000
