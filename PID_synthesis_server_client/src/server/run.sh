#!/bin/bash

## Global parameters
source $( dirname $0 )/../../bash/functions.sh

define_from_config local_path SERVER_PATH
define_from_config local_path SERVER_LOG_PATH
define_from_config server_URL SERVER_URL
define_from_config server_port SERVER_PORT
define_from_config python_env PYTHON_ENV

## Constants
declare -r KSIG='15' # SIGTERM

if lsof -t -i:$SERVER_PORT
then
    kill -s $KSIG $( lsof -t -i:$SERVER_PORT )
    
    echo "$( date ): Dirty initialize because port was in use." >> \
	 $SERVER_LOG_PATH/initialize.log
fi

# screen -d -m -S PID_synthesis_server_daemon \
    until $PYTHON_ENV $SERVER_PATH/src/server/server.py \
		      $SERVER_URL $SERVER_PORT
    do
	sleep 4
    done
       
       
echo "$( date ): Initialization success" >> \
     $SERVER_LOG_PATH/initialize.log    


exit 0
