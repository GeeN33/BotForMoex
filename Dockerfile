FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Обновление списка пакетов и установка необходимых пакетов
RUN apt update && \
    apt install -y make automake gcc g++ subversion python3-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .


#CMD ["/bin/sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8733"]

CMD ["/bin/sh", "-c", "python manage.py migrate && gunicorn --workers 4 --threads 4 --bind 0.0.0.0:8733 core.wsgi:application --log-level info"]