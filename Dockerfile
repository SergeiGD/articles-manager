FROM python:3.10.10-alpine3.17

WORKDIR /app

RUN apk update && apk add bash postgresql-dev gcc python3-dev musl-dev nano

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD     ./wait-for-it.sh db:5432 -- \
        python3 manage.py makemigrations && \
        python3 manage.py migrate && \
        python3 manage.py runserver 0.0.0.0:8000

