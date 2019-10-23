#!/bin/bash

#
# Compute all possible controllers configurations
#
#

## Global parameters
source $( dirname $0 )/../../bash/functions.sh

define_from_config local_path SERVER_PATH
define_from_config python_env PYTHON_ENV

SYNTAX='m_code'
if [[ $5 ]]; then SYNTAX="$5" ; fi

declare -i TOTAL_ERROR=1
declare -i ERROR

for CONTROLLER in PI PID
do
    for SENSIBILITY in 1.4 2.0
    do
	$PYTHON_ENV $SERVER_PATH/src/tunning/tunning.py \
		    $1 $2 $3 $4 $SENSIBILITY $SYNTAX $CONTROLLER
	ERROR=$?
	if (( $ERROR ))
	then
	    [[ $SYNTAX == 'm_code' ]] &&
		printf "${CONTROLLER}_Ms_${SENSIBILITY/\./_}_enable=false;\n"
	else
	    [[ $SYNTAX == 'm_code' ]] &&
		printf "${CONTROLLER}_Ms_${SENSIBILITY/\./_}_enable=true;\n"
	fi
	TOTAL_ERROR=$(( ERROR*TOTAL_ERROR )) # Zero if there is at least one solution
    done
done
if (( TOTAL_ERROR ))
then
    echo '% System have no solutions
% Values out of range'
fi
exit $TOTAL_ERROR
