#!/bin/bash

# Script receive params and use the
# required sketcher
#
# $1 => cache_dir
# 

## Global server parameters
declare DEFAULT_CONFIG_FILE="$HOME/.pid_ss.conf"
declare SERVER_PATH="$( grep '^local_path' $DEFAULT_CONFIG_FILE | cut -f 2 )"

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
run $SERVER_PATH/src/sketcher/lib/start.m
run $M_CACHE_PATH/parameters.m
run $SERVER_PATH/src/sketcher/sys_response.m
run $SERVER_PATH/src/sketcher/lib/finish.m
" > $M_CACHE_PATH/script.m

## Execute only one command
printf 'Using sketcher\n'
run_matlab_command 'matlab_socket_1' 'run '$M_CACHE_PATH'/script.m;'

exit 0
