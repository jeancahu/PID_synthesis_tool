%% Compare models

step(sys_model_POMTM_alfaro123c);
hold on;
step(sys_model_POMTM_broida)
hold on;
step(sys_model_POMTM_ho_et_al)
hold on;
step(sys_model_POMTM_chen_y_yang)
hold on;
step(sys_model_POMTM_smith)
hold on;
step(sys_model_POMTM_viteckova_et_al)

hold on;
step(sys_model_PDMTM_alfaro123c)
hold on;
step(sys_model_PDMTM_ho_et_al)
hold on;
step(sys_model_PDMTM_viteckova_et_al)

hold on;
step(sys_model_SOMTM_alfaro123c)
hold on;
step(sys_model_SOMTM_stark)

legend('sys\_model\_POMTM\_alfaro123c',...
'sys\_model\_POMTM\_broida',...
'sys\_model\_POMTM\_ho\_et\_al',...
'sys\_model\_POMTM\_chen\_y\_yang',...
'sys\_model\_POMTM\_smith',...
'sys\_model\_POMTM\_viteckova\_et\_al',...
'sys\_model\_PDMTM\_alfaro123c',...
'sys\_model\_PDMTM\_ho\_et\_al',...
'sys\_model\_PDMTM\_viteckova\_et\_al',...
'sys\_model\_SOMTM\_alfaro123c',...
'sys\_model\_SOMTM\_stark')
