#/bin/bash

export TF="../../data/title.basics.tsv"

START=0
STOP=$(($START + 100000))
MAX=7000000

while test $START -le $MAX
do
	echo ${START} - ${STOP}
	./manage.py loadtitles --path ${TF} --rowstart ${START} --rowstop ${STOP} &
	START=$STOP
	STOP=$(($START + 250000))
done

