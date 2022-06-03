#!/bin/bash

# Server mode flags
MATLAB_FLAGS='-nosplash -nodesktop -nodisplay'
MATLAB_SESSION='matlab_socket_1'

if screen -list $MATLAB_SESSION &>/dev/null
then
    :
else
    screen -dm -S $MATLAB_SESSION matlab $MATLAB_FLAGS
fi

exit 0
