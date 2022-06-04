#!/bin/bash

declare DIR_CACHE=$1

until test -f $DIR_CACHE/ready.txt && grep -c 'model_comparison_ready' $1/ready.txt &>/dev/null
do sleep 0.01 ; done

printf "var vect_tnorm = [ $( cut -f 1 ${DIR_CACHE}/model_step_response.txt | tr '\n' ',' )]\n" | sed 's/,]$/];/'
printf "var vect_unorm = [ $( cut -f 2 ${DIR_CACHE}/model_step_response.txt | tr '\n' ',' )]\n" | sed 's/,]$/];/'
printf "var vect_ynorm = [ $( cut -f 3 ${DIR_CACHE}/model_step_response.txt | tr '\n' ',' )]\n" | sed 's/,]$/];/'
printf "var vect_ym = [ $( cut -f 4 ${DIR_CACHE}/model_step_response.txt | tr '\n' ',' )]\n" | sed 's/,]$/];/'


exit 0
