%
% Define controllers
%
%

fprintf("Running define controllers module\n")

%% PI 1.4 Ms
if PI_Ms_1_4_enable
    PI_Ms_1_4 = action*PI_Ms_1_4_K_p*(1 + (1/(PI_Ms_1_4_T_i*s)));
end

%% PI 2.0 Ms
if PI_Ms_2_0_enable
    PI_Ms_2_0 = action*PI_Ms_2_0_K_p*(1 + (1/(PI_Ms_2_0_T_i*s)));
end

%% PID ODoL 1.4 Ms
if PID_Ms_1_4_enable
    PID_Ms_1_4 = action*PID_Ms_1_4_K_p*( 1 + (1/(PID_Ms_1_4_T_i*s)) + ((PID_Ms_1_4_T_d*s)/(1+a*PID_Ms_1_4_T_d*s)) );
end

%% PID ODoL 2.0 Ms
if PID_Ms_2_0_enable
    PID_Ms_2_0 = action*PID_Ms_2_0_K_p*( 1 + (1/(PID_Ms_2_0_T_i*s)) + ((PID_Ms_2_0_T_d*s)/(1+a*PID_Ms_2_0_T_d*s)) );
end