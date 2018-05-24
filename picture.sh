#!/bin/bash

kuva="/var/www/html/data/kuva.jpg"
old="/var/www/html/data/old/kuva_$(date -d "today" +"%Y%m%d_%H").jpg"

if [[ -f ${kuva} ]]; then
    if [[ ! -f ${old} ]]; then
        mv $kuva $old
    fi
fi

/usr/bin/raspistill -w 800 -h 600 -t 1 -o ${kuva}
