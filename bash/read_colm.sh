#!/bin/bash

[ $1 ] || exit 1

declare -i COUNT=1

sed 's/ /\n/g;/^$/d' </dev/stdin |

while read LINE
do
    if (( COUNT == $1 ))
    then
	let COUNT=0
	echo "$LINE"
    else
	echo -ne "$LINE\t"
    fi

    let COUNT++
    
done

exit 0
