#!/bin/bash

until test -f $1/ready.txt
do sleep 0.01 ; done

for IMAGE in $1/*.png
do
    if [ -f "$IMAGE" ]
    then
	printf ','"$( basename $IMAGE )"    
    fi
done

exit 0
