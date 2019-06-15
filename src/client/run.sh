#!/bin/bash

declare DEFAULT_CONFIG_FILE="$HOME/.pid_ss.conf"
declare SERVER_LOG_PATH="$( grep '^local_path' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare SERVER_PORT="$( grep '^server_port' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare SERVER_URL="$( grep '^server_URL' $DEFAULT_CONFIG_FILE | cut -f 2 )"
declare KSIG='15' # SIGTERM

echo "$( date ): Executing client test code." >> \
     $SERVER_LOG_PATH/initialize.log

$SERVER_LOG_PATH/src/client/client.py $SERVER_URL $SERVER_PORT

echo "$( date ): Client execution success." >> \
     $SERVER_LOG_PATH/initialize.log    


exit 0
