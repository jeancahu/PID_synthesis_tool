#!/bin/bash

#
# Compute all possible controllers configurations
#
#

declare DEFAULT_CONFIG_FILE="$HOME/.pid_ss.conf"
declare SERVER_PATH="$( grep '^local_path' $DEFAULT_CONFIG_FILE | cut -f 2 )"
#declare SERVER_PORT="$( grep '^server_port' $DEFAULT_CONFIG_FILE | cut -f 2 )"
#declare SERVER_URL="$( grep '^server_URL' $DEFAULT_CONFIG_FILE | cut -f 2 )"
#declare KSIG='15' # SIGTERM

MATLAB_SYNTAX=True
if [[ $5 =~ 'False' ]]; then MATLAB_SYNTAX=False ; fi

for CONTROLLER in PI PID
do
    for SENSIBILITY in 1.4 2.0
    do
	$SERVER_PATH/src/tunning/tunning.py $1 $2 $3 $4 $SENSIBILITY $MATLAB_SYNTAX $CONTROLLER
	if (( $? ))
	then
	    [[ $5 == 'False' ]] || printf "${CONTROLLER}_Ms_${SENSIBILITY/\./_}_enable=false;\n"
	else
	    [[ $5 == 'False' ]] || printf "${CONTROLLER}_Ms_${SENSIBILITY/\./_}_enable=true;\n"
	fi
    done
done

exit 0
