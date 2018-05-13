#!/bin/bash

APP_NAME=$1
ROOT_DIR=$2
VENV_NAME=$3
WORKER_COUNT=$4
HOST=$5
PORT=$6
WSGI_FILE=$7
WSGI_OBJ=$8
PID_FILE=$9


cd $ROOT_DIR
source $ROOT_DIR$VENV_NAME/bin/activate
nohup gunicorn -w $WORKER_COUNT -b $HOST:$PORT $WSGI_FILE:$WSGI_OBJ> /dev/null 2>&1 & echo $! > ${PID_FILE}
