#!/bin/bash
i=0
while :
do
	d=`date +%Y-%M-%d\ %H:%M:%S`
	echo "$d loop: $i"
	./readDensirtyFile.py /media/Cygno/northdome_record.csv
	echo "Press [CTRL+C] to stop.."
	i=$((i+1))
	sleep 60
done
