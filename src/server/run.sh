#!/bin/bash

declare SERVER_PORT="8494"
declare KSIG='15' # SIGTERM
declare SERVER_LOG_PATH=$HOME/PID_synthesis_server_client

if lsof -t -i:$SERVER_PORT
then
    kill -s $KSIG $( lsof -t -i:$SERVER_PORT )
    
    echo "$( date ): Dirty initialize because port was in use." >> \
	 $SERVER_LOG_PATH/initialize.log
fi

# screen -d -m -S PID_synthesis_server_daemon $SERVER_LOG_PATH/src/server/server.py
$SERVER_LOG_PATH/src/server/server.py

echo "$( date ): Initialization success" >> \
     $SERVER_LOG_PATH/initialize.log    


exit 0
