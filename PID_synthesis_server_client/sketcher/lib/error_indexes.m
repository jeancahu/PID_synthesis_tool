TMIN=0; % FIXME

file_erridx_id = fopen(output_path+"error_indexes.txt", "wt");

err_min_step = min([X1_t(2) X2_t(2) X3_t(2) X4_t(2)]);
err_index_temp_time = [TMIN:err_min_step:TMAX];

fprintf(file_erridx_id, '{\n');
fprintf(file_erridx_id, '\t"type": "error_indexes"');

%% PI 1.4 Ms
if PI_Ms_1_4_enable
    IAE_r = sum(abs(step(Myr_PI_Ms_1_4,err_index_temp_time)-1));
    IAE_d = sum(abs(step(Myd_PI_Ms_1_4,err_index_temp_time)));
    TOTAL_IAE=IAE_r+IAE_d

    fprintf(file_erridx_id, ',\n\t"IAE_R_PI_1_4": %.4f', IAE_r);     % Reference error
    fprintf(file_erridx_id, ',\n\t"IAE_D_PI_1_4": %.4f', IAE_d);     % Disturbance error
    fprintf(file_erridx_id, ',\n\t"IAE_T_PI_1_4": %.4f', TOTAL_IAE); % Total error
end

%% PI 2.0 Ms
if PI_Ms_2_0_enable
    IAE_r = sum(abs(step(Myr_PI_Ms_2_0,err_index_temp_time)-1));
    IAE_d = sum(abs(step(Myd_PI_Ms_2_0,err_index_temp_time)));
    TOTAL_IAE=IAE_r+IAE_d

    fprintf(file_erridx_id, ',\n\t"IAE_R_PI_2_0": %.4f', IAE_r);     % Reference error
    fprintf(file_erridx_id, ',\n\t"IAE_D_PI_2_0": %.4f', IAE_d);     % Disturbance error
    fprintf(file_erridx_id, ',\n\t"IAE_T_PI_2_0": %.4f', TOTAL_IAE); % Total error
end

%% PID ODoL 1.4 Ms
if PID_Ms_1_4_enable
    IAE_r = sum(abs(step(Myr_PID_Ms_1_4,err_index_temp_time)-1));
    IAE_d = sum(abs(step(Myd_PID_Ms_1_4,err_index_temp_time)));
    TOTAL_IAE=IAE_r+IAE_d

    fprintf(file_erridx_id, ',\n\t"IAE_R_PID_1_4": %.4f', IAE_r);     % Reference error
    fprintf(file_erridx_id, ',\n\t"IAE_D_PID_1_4": %.4f', IAE_d);     % Disturbance error
    fprintf(file_erridx_id, ',\n\t"IAE_T_PID_1_4": %.4f', TOTAL_IAE); % Total error
end

%% PID ODoL 2.0 Ms
if PID_Ms_2_0_enable
    IAE_r = sum(abs(step(Myr_PID_Ms_2_0,err_index_temp_time)-1));
    IAE_d = sum(abs(step(Myd_PID_Ms_2_0,err_index_temp_time)));
    TOTAL_IAE=IAE_r+IAE_d

    fprintf(file_erridx_id, ',\n\t"IAE_R_PID_2_0": %.4f', IAE_r);     % Reference error
    fprintf(file_erridx_id, ',\n\t"IAE_D_PID_2_0": %.4f', IAE_d);     % Disturbance error
    fprintf(file_erridx_id, ',\n\t"IAE_T_PID_2_0": %.4f', TOTAL_IAE); % Total error
end

%% Close JSON object
fprintf(file_erridx_id, '\n}');

file_id = fopen(output_path+"ready.txt", "a+");
fprintf(file_id,'error_indexes_ready\n');
fclose(file_id);