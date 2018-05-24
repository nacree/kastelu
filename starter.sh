#!/bin/bash

program=$1

if [[ -z $program ]]
then 
    echo "argument empty"
    exit
fi

test=$(ps aux | grep ${program} | grep -v grep | grep -v starter.sh)

if [[ -z $test ]]
then
    echo "starting program"
    /usr/bin/python /home/nacre/kastelu/${program}.py & >> /home/nacre/kastelu/logs/${program}.log 2>&1
else
    echo "program rumming"
fi
