#!/bin/bash

# Backgroud process
# Generate plots
#

## Global parameters
source $( dirname $0 )/functions.sh

define_from_config local_path SERVER_PATH
define_from_config cache_path CACHE_PATH

## Local variables
FRA_ORDER="$1"
TIME_CONS="$2"
PROP_CONS="$3"
DEAD_TIME="$4"

if [ "$*" ]
then
    SIMU_DIR="$(
    printf "$FRA_ORDER,$TIME_CONS,$PROP_CONS,$DEAD_TIME" |
	md5sum | cut -f 1 -d ' ' )"
else
    STEP_RESPONSE="$( cat /dev/stdin )"
    SIMU_DIR="$(
    printf "$STEP_RESPONSE" |
	md5sum | cut -f 1 -d ' ' )"
fi

## Verify if simulation already exist
if [ -d ${CACHE_PATH}/${SIMU_DIR} ]
then
    :
    #printf 'There is a directory\n'
    #exit 0 # FIXME
else
    #printf 'There is not a directory\n'
    mkdir -p ${CACHE_PATH}/${SIMU_DIR}
fi

## Cache dir to standard output
printf "${CACHE_PATH}/${SIMU_DIR}\n"

## Save step sys response
printf "${STEP_RESPONSE}\n" \
       > ${CACHE_PATH}/${SIMU_DIR}/step_response.txt

## Generate results table
{
    $SERVER_PATH/src/tunning/run.sh \
	$FRA_ORDER $TIME_CONS $PROP_CONS $DEAD_TIME False \
	> ${CACHE_PATH}/${SIMU_DIR}/results_table.txt \
	2> ${CACHE_PATH}/${SIMU_DIR}/error_log.txt
    if (( $? )) # If there are not solutions then send error log
    then
	{
	printf '\n\n'
	grep '^ValueError' \
	     ${CACHE_PATH}/${SIMU_DIR}/error_log.txt |
	    uniq
	} >> ${CACHE_PATH}/${SIMU_DIR}/results_table.txt
    fi
}&

## Generate matlab parameters header
{
## Add process params
printf "v=$FRA_ORDER;T=$TIME_CONS;K=$PROP_CONS;L=$DEAD_TIME;\n"

## Add controller params
$SERVER_PATH/src/tunning/run.sh $FRA_ORDER $TIME_CONS $PROP_CONS $DEAD_TIME

## Setting outfiles path
printf "output_path='${CACHE_PATH}/${SIMU_DIR}/';\n"

} > ${CACHE_PATH}/${SIMU_DIR}/parameters.m

## Run the sketcher program
$SERVER_PATH/src/sketcher/run.sh ${CACHE_PATH}/${SIMU_DIR} &>/dev/null

exit 0
