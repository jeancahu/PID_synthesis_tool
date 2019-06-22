#!/bin/bash

## Global parameters
source $( dirname $0 )/../../bash/functions.sh

define_from_config local_path SERVER_PATH
define_from_config local_path SERVER_LOG_PATH
define_from_config server_URL SERVER_URL
define_from_config server_port SERVER_PORT
define_from_config python_env PYTHON_ENV

## Local constants
declare -r KSIG='15' # SIGTERM

echo "$( date ): Executing client test code." >> \
     $SERVER_LOG_PATH/initialize.log

$PYTHON_ENV $SERVER_PATH/src/client/client.py $SERVER_URL $SERVER_PORT

echo "$( date ): Client execution success." >> \
     $SERVER_LOG_PATH/initialize.log    


exit 0
