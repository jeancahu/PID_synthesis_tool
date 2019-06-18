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

for CONTROLLER in PI PID
do
    for SENSIBILITY in 1.4 2.0
    do
	$SERVER_PATH/src/tunning/tunning.py $1 $2 $3 $4 $SENSIBILITY True $CONTROLLER
	if (( $? ))
	then
	    printf "${CONTROLLER}_${SENSIBILITY/\./_}=false;\n"
	else
	    printf "${CONTROLLER}_${SENSIBILITY/\./_}=true;\n"
	fi
    done
done

exit 0
