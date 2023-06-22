FROM ubuntu/apache2:2.4-20.04_edge

WORKDIR /app

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.10 python3-pip python3-dev libpq-dev libapache2-mod-wsgi-py3 nano netcat

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./articles.conf /etc/apache2/sites-available/articles.conf
RUN a2enmod headers && service apache2 restart
RUN a2ensite articles.conf
RUN a2dissite 000-default.conf
EXPOSE 80

COPY entrypoint.sh /app_scripts/entrypoint.sh
RUN sed -i 's/\r$//g' /app_scripts/entrypoint.sh
RUN chmod +x /app_scripts/entrypoint.sh

CMD /app_scripts/entrypoint.sh

#RUN sed -i 's/\r$//g' /app/entrypoint.sh
#RUN chmod +x /app/entrypoint.sh
#
#CMD /app/entrypoint.sh


#FROM ubuntu
#
#RUN apt-get update
#RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
#RUN apt-get -y install python3 libapache2-mod-wsgi-py3
#RUN ln /usr/bin/python3 /usr/bin/python
#RUN apt-get -y install python3-pip
#RUN ln /usr/bin/pip3 /usr/bin/pip
#RUN pip install --upgrade pip
#COPY ./requirements.txt .
#RUN pip install -r requirements.txt
#ADD ./articles.conf /etc/apache2/sites-available/articles.conf
#RUN a2ensite crystal_lake.conf
#RUN a2dissite 000-default.conf
#RUN a2enmod headers && service apache2 restart
#EXPOSE 80 3500
#CMD ["apache2ctl", "-D", "FOREGROUND"]


#FROM python:3.10.10-alpine3.17
#
#WORKDIR /app
#
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev nano
#
#RUN pip install --upgrade pip
#COPY ./requirements.txt .
#RUN pip install -r requirements.txt
#
#EXPOSE 8000
#EXPOSE 466
#
#CMD     python3 manage.py makemigrations && \
#        python3 manage.py migrate && \
#        python3 manage.py runserver 0.0.0.0:8000
