#!/bin/bash

until test -f $1/ready.txt && grep -c 'simulations_images_ready' $1/ready.txt &>/dev/null
do sleep 0.01 ; done

for IMAGE in $1/*.png
do
    if [ -r "$IMAGE" ]
    then
	printf ','"$( basename $IMAGE )"    
    fi
done

exit 0
