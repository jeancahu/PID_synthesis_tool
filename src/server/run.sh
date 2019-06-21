#!/bin/bash

declare DEFAULT_CONFIG_FILE="$HOME/.pid_ss.conf"
declare SERVER_LOG_PATH="$( grep '^local_path' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare SERVER_PORT="$( grep '^server_port' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare SERVER_URL="$( grep '^server_URL' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare KSIG='15' # SIGTERM

if lsof -t -i:$SERVER_PORT
then
    kill -s $KSIG $( lsof -t -i:$SERVER_PORT )
    
    echo "$( date ): Dirty initialize because port was in use." >> \
	 $SERVER_LOG_PATH/initialize.log
fi

# screen -d -m -S PID_synthesis_server_daemon \
until $SERVER_LOG_PATH/src/server/server.py $SERVER_URL $SERVER_PORT
do
    sleep 4
done
       
       
echo "$( date ): Initialization success" >> \
     $SERVER_LOG_PATH/initialize.log    


exit 0
