%
% Define close loop transfer functions
%
%

fprintf("Running close loop transfer functions define module\n")

%% PI 1.4 Ms
if PI_Ms_1_4_enable
    Myd_PI_Ms_1_4 = Pm/(1+PI_Ms_1_4*Pm);
    Myr_PI_Ms_1_4 = PI_Ms_1_4*Pm/(1+PI_Ms_1_4*Pm);
end

%% PI 2.0 Ms
if PI_Ms_2_0_enable
    Myd_PI_Ms_2_0 = Pm/(1+PI_Ms_2_0*Pm);
    Myr_PI_Ms_2_0 = PI_Ms_2_0*Pm/(1+PI_Ms_2_0*Pm);
end

%% PID ODoL 1.4 Ms
if PID_Ms_1_4_enable
    Myd_PID_Ms_1_4 = Pm/(1+PID_Ms_1_4*Pm);
    Myr_PID_Ms_1_4 = PID_Ms_1_4*Pm/(1+PID_Ms_1_4*Pm);
end

%% PID ODoL 2.0 Ms
if PID_Ms_2_0_enable
    Myd_PID_Ms_2_0 = Pm/(1+PID_Ms_2_0*Pm);
    Myr_PID_Ms_2_0 = PID_Ms_2_0*Pm/(1+PID_Ms_2_0*Pm);
end
