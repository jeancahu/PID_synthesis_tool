#!/bin/bash

# Backgroud process
# Generate plots
#

## Global parameters
declare DEFAULT_CONFIG_FILE="$HOME/.pid_ss.conf"
declare SERVER_PATH="$( grep '^local_path' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare CACHE_PATH="$( grep '^cache_path' $DEFAULT_CONFIG_FILE | cut -f 2 )"

## Local variables
FRA_ORDER="$1"
TIME_CONS="$2"
PROP_CONS="$3"
DEAD_TIME="$4"

SIMU_DIR="$(
    printf "$FRA_ORDER,$TIME_CONS,$PROP_CONS,$DEAD_TIME" |
	md5sum | cut -f 1 -d ' ' )"


## Verify if simulation already exist
if [ -d ${CACHE_PATH}/${SIMU_DIR} ]
then
    printf 'There is a directory\n'
    #exit 0 # FIXME
else
    printf 'There is not a directory\n'
    mkdir -p ${CACHE_PATH}/${SIMU_DIR}
fi

{
## Add process params
printf "v=$FRA_ORDER;T=$TIME_CONS;K=$PROP_CONS;L=$DEAD_TIME;\n"

## Add controller params
$SERVER_PATH/src/tunning/run.sh $FRA_ORDER $TIME_CONS $PROP_CONS $DEAD_TIME

## Setting outfiles path
printf "output_path='${CACHE_PATH}/${SIMU_DIR}/';\n"

} > ${CACHE_PATH}/${SIMU_DIR}/parameters.m

## Run the sketcher program
$SERVER_PATH/src/sketcher/run.sh ${CACHE_PATH}/${SIMU_DIR}

exit 0
