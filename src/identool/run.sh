#!/bin/bash

# Script receive params and use the
# required identool
#
# $1 => cache_dir
# 

## Global server parameters
source $( dirname $0 )/../../bash/functions.sh

define_from_config local_path SERVER_PATH

## Local vars
M_CACHE_PATH=$1

## Functions
function run_matlab_command () {
    #
    # $1 session name
    # $2 command
    screen -S "$1" -X stuff "$2\r"
}

# Test cache directory exist
{ [ $M_CACHE_PATH ] && [ -d $M_CACHE_PATH ]; } ||
    { printf 'Error, cache directory not found\n' &>/dev/stderr ; exit 1; }

printf "output_path='$M_CACHE_PATH/';\n" >> $M_CACHE_PATH/parameters.m


# Generate script
printf "
run $SERVER_PATH/src/identool/lib/start.m
run $M_CACHE_PATH/parameters.m
run $SERVER_PATH/src/identool/lib/set_variables.m
run $SERVER_PATH/src/identool/lib/IDFOM.m
run $SERVER_PATH/src/identool/lib/finish.m
" > $M_CACHE_PATH/identool.m

## Execute only one command
printf 'Using identool\n'
run_matlab_command 'matlab_socket_1' 'run '$M_CACHE_PATH'/identool.m;'

exit 0
