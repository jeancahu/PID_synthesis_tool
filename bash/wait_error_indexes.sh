#!/bin/bash

declare DIR_CACHE=$1

until test -f $DIR_CACHE/ready.txt && grep -c 'error_indexes_ready' $1/ready.txt &>/dev/null
do sleep 0.01 ; done

exit 0
