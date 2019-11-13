TMIN=0; % FIXME

err_min_step = min([X1_t(2) X2_t(2) X3_t(2) X4_t(2)])
err_index_temp_time = [TMIN:err_min_step:TMAX]

%% PI 1.4 Ms
if PI_Ms_1_4_enable
    IAE_r = sum(abs(step(Myr_PI_Ms_1_4*k_Ref,err_index_temp_time)))
    IAE_d = sum(abs(step(Myd_PI_Ms_1_4*k_Per,err_index_temp_time)))
end

%% PI 2.0 Ms
if PI_Ms_2_0_enable
    IAE_r = sum(abs(step(Myr_PI_Ms_2_0*k_Ref,err_index_temp_time)))
    IAE_d = sum(abs(step(Myd_PI_Ms_2_0*k_Per,err_index_temp_time)))
end

%% PID ODoL 1.4 Ms
if PID_Ms_1_4_enable
    IAE_r = sum(abs(step(Myr_PID_Ms_1_4*k_Ref,err_index_temp_time)))
    IAE_d = sum(abs(step(Myd_PID_Ms_1_4*k_Per,err_index_temp_time)))
end

%% PID ODoL 2.0 Ms
if PID_Ms_2_0_enable
    IAE_r = sum(abs(step(Myr_PID_Ms_2_0*k_Ref,err_index_temp_time)))
    IAE_d = sum(abs(step(Myd_PID_Ms_2_0*k_Per,err_index_temp_time)))
end
