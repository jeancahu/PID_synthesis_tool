#!/bin/bash

declare DIR_CACHE=$1

until test -f $DIR_CACHE/ready.txt && grep -c 'simulations_vectors_ready' $1/ready.txt &>/dev/null
do sleep 0.01 ; done

for VECT in X1 X2 X3 X4 R D
do
    printf "var vect_${VECT}_t = [ $( cut -f 1 ${DIR_CACHE}/${VECT}.txt | tr '\n' ',' )]\n" | sed 's/,]$/];/'
    printf "var vect_${VECT} = [ $( cut -f 2 ${DIR_CACHE}/${VECT}.txt | tr '\n' ',' )]\n" | sed 's/,]$/];/'
done

exit 0
