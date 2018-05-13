#!/bin/bash

APP_NAME=$1
PID_FILE=$2
LOCK_FILE=$3
PID=`cat $PID_FILE`

PID_LIST=`ps -ef | grep "$APP_NAME" | grep -v grep | awk '{print $2}'`
echo $PID_LIST

kill -9 $PID
# kill -9 $PID_LIST

for((i=1;i<=100;i++));  
do   
    # EXISTS_PID=`ps aux  | awk '{print $2}' | grep $PID`
    EXISTS_PID=`ps -ef | grep "$APP_NAME" | grep -v grep | awk '{print $2}'`
    echo $EXISTS_PID
    if [ ! -n "$EXISTS_PID" ]; then
        echo $EXISTS_PID
        echo 'delete!!'
        rm $PID_FILE
        rm $LOCK_FILE
        break
    fi
    sleep 1
    echo 'sleep'

done