#!/bin/bash

# Generate python3 dicts from plain text tables

# Args:
# * $1 : Data table PI?_*:?.?.txt filesystem path

declare DICT_NAME=$( basename $1 )
DICT_NAME=${DICT_NAME/tables_data_/}
DICT_NAME=${DICT_NAME/.txt/}
DICT_NAME=${DICT_NAME/\./_}

[ -f $1 ] || exit 1

CONST_NAMES=( $( cut -f 1 $1 | tail -n $(( $( wc -l <$1 ) -1 )) ) )
FRACT_VALS=( $( head -n 1 $1 | cut -f 2- ) )

printf  "
${DICT_NAME} = {

"

COUNTER_COL=2
for FRACT_VAL in ${FRACT_VALS[@]}
do
    printf ",
    '$FRACT_VAL': {
"

    COUNTER_ROW=0
    CONST_VALUES=( $( cut -f $COUNTER_COL $1 | tail -n ${#CONST_NAMES[@]} ) )
    for CONST in ${CONST_NAMES[@]}
    do
	printf ",
        \x27$CONST\x27 : ${CONST_VALUES[$COUNTER_ROW]}"
	let COUNTER_ROW++
    done

    printf "
    }"
    let COUNTER_COL++
done | sed '/^,$/d'
    
    printf "
}
"

exit 0
