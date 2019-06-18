#!/bin/bash

# Server mode flags
MATLAB_FLAGS='-nosplash -nodesktop -nodisplay'

#screen -d -m -S matlab_daemon matlab $MATLAB_FLAGS > $HOME/matlab_pipes
matlab $MATLAB_FLAGS < $HOME/matlab_pipes/in > $HOME/matlab_pipes/out &


exit 0
