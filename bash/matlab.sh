#!/bin/bash

#screen -d -m -S matlab_daemon matlab -nojvm -nosplash > $HOME/matlab_pipes
matlab -nojvm -nosplash < $HOME/matlab_pipes/in > $HOME/matlab_pipes/out &


exit 0
