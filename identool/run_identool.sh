#!/bin/bash

if [ "$1" == '' ]
then
    echo 'Error, no se definió la función de transferencia'
    exit 1
fi

echo "
% Este script obtiene la respuesta al escalón de un proceso
% Jeancarlo Hidalgo Ureña <jeancahu@gmail.com>
%%
s=tf('s');
P_real=""$1""
[M,t]=step(P_real);
%plot(t,M)
%hold on;
M_dt=M.*(M > 0);
Y=M_dt;
writetable(array2table( [transpose(Y) ; transpose(t) ]), 'system_response.csv')
" > generate_step_response.m

# Ejecución en matlab
matlab -nodisplay -nodesktop -nojvm -nosplash -r 'generate_step_response; exit'

tail -n 2 system_response.csv > file_temporal_system_response.csv

python2.7 identool.py file_temporal_system_response.csv > result.txt
cat result.txt

bash convert_to_matlab_sintax.sh

exit 0
