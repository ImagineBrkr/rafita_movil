#!/bin/bash

pip install -r requirements.txt

LOG_FILE="./logs"
python3 manage.py makemigrations
python3 manage.py makemigrations ComprasApp
python3 manage.py makemigrations PedidosApp
python3 manage.py makemigrations CajaApp
python3 manage.py migrate
APP_CMD="nice -n-20 python3 manage.py runserver 0.0.0.0:8000 >> $LOG_FILE 2>&1 &"
start_app() {
    eval $APP_CMD
    echo "App started"
}

start_app