#!/bin/bash

echo '%% System Models' > system_models.m
echo "s=tf('s');" >> system_models.m

CONT=0

for CONST in $( cat result.txt | grep '^ ' | grep -v '\-\-\-' | uniq | sed 's/s + 1//g' | sed 's/)(/\n/g' | sed 's/e\^(/\n/g' | sed 's/ //g' | sed 's/[()s]//g' | sed 's/\^2//g' | grep -v '^$' )
do
    echo 'TEMP'"$CONT"'='"$CONST"';' >> system_models.m
    CONT=$(( $CONT + 1 ))
done

echo "

sys_model_POMTM_alfaro123c=TEMP0*exp(TEMP1*s)/(TEMP2*s+1);
sys_model_POMTM_broida=TEMP3*exp(TEMP4*s)/(TEMP5*s+1);
sys_model_POMTM_ho_et_al=TEMP6*exp(TEMP7*s)/(TEMP8*s+1);
sys_model_POMTM_chen_y_yang=TEMP9*exp(TEMP10*s)/(TEMP11*s+1);
sys_model_POMTM_smith=TEMP12*exp(TEMP13*s)/(TEMP14*s+1);
sys_model_POMTM_viteckova_et_al=TEMP15*exp(TEMP16*s)/(TEMP17*s+1);

sys_model_PDMTM_alfaro123c=TEMP18*exp(TEMP19*s)/((TEMP20*s+1)^2);
sys_model_PDMTM_ho_et_al=TEMP21*exp(TEMP22*s)/((TEMP23*s+1)^2);
sys_model_PDMTM_viteckova_et_al=TEMP24*exp(TEMP25*s)/((TEMP26*s+1)^2);

sys_model_SOMTM_alfaro123c=TEMP27*exp(TEMP28*s)/((TEMP29*s+1)*(TEMP30*s+1));
sys_model_SOMTM_stark=TEMP31*exp(TEMP32*s)/((TEMP33*s+1)*(TEMP34*s+1));
" >> system_models.m

cat system_models.m

exit 0
