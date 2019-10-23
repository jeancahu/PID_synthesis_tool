#!/bin/bash

# Backgroud process
# Generate plots
#

## Global parameters
source $( dirname $0 )/functions.sh

define_from_config local_path SERVER_PATH
define_from_config cache_path CACHE_PATH

## Local variables
SYNTAX="$1"
FRA_ORDER="$2"
TIME_CONS="$3"
PROP_CONS="$4"
DEAD_TIME="$5"

if [ $FRA_ORDER ] && [ $TIME_CONS ] && [ $PROP_CONS ] && [ $DEAD_TIME ]
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

## Cache dir to standard output
printf "${CACHE_PATH}/${SIMU_DIR}\n"

## Verify if simulation already exist
if [ -d ${CACHE_PATH}/${SIMU_DIR} ]
then
    :
    # There is a directory
    # TODO: verify data
    #exit 0
else
    # There is not a directory
    mkdir -p ${CACHE_PATH}/${SIMU_DIR}
fi

## Save step sys response
printf "${STEP_RESPONSE}\n" \
       > ${CACHE_PATH}/${SIMU_DIR}/step_response.txt

## Using identool if there are not input parameters
if [ $FRA_ORDER ] && [ $TIME_CONS ] && [ $PROP_CONS ] && [ $DEAD_TIME ]
then
    :
else
    ## Run the identool program

    ## Setting outfiles path
    printf "output_path='${CACHE_PATH}/${SIMU_DIR}/';\n" \
	   > ${CACHE_PATH}/${SIMU_DIR}/parameters.m

    $SERVER_PATH/src/identool/run.sh ${CACHE_PATH}/${SIMU_DIR} &>/dev/null
    until grep 'model_calculated_values' \
	       ${CACHE_PATH}/${SIMU_DIR}/identool_results.m &>/dev/null
    do
	sleep 0.1
    done
    PARAMS=( $(
		 sed 's/.=//g;s/ .*//;s/;/\t/g' \
		     <${CACHE_PATH}/${SIMU_DIR}/identool_results.m
	     )  )
    # Setting the new identified parameters
    FRA_ORDER=${PARAMS[0]}
    TIME_CONS=${PARAMS[1]}
    PROP_CONS=${PARAMS[2]}
    DEAD_TIME=${PARAMS[3]}
fi

## Generate results table
{
    $SERVER_PATH/src/tunning/run.sh \
	$FRA_ORDER $TIME_CONS $PROP_CONS $DEAD_TIME $SYNTAX \
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
