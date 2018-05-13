#!/bin/bash

APP_NAME=$1
PID_FILE=$2
LOCK_FILE=$3
PID=`cat $PID_FILE`

kill -9 $PID

for((i=1;i<=100;i++));  
do   
    # EXISTS_PID=`ps -ef | grep "$APP_NAME.*gunicorn" | grep -v grep | awk '{print $2}'`
    if [ ! -n "`ps -ef | grep "$APP_NAME.*gunicorn" | grep -v grep | awk '{print $2}'`" ]; then
        rm $PID_FILE
        rm $LOCK_FILE
        break
    fi
    sleep 1
done