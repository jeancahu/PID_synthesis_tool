
END=100*T; % Tiempo de simulacion, segundos, proporcional a T_planta

%% Definicion de la salida, y perturbaciones:
TREF=0.24*END; % tiempo en que ocurre R
TPER=0.7*END; % tiempo en que ocurre D

t=[0:0.001:END];
R=k_Ref*exp(-TREF*s);
D=k_Per*exp(-TPER*s);

%% PI 1.4 Ms
if PI_Ms_1_4_enable
    Y_PI_Ms_1_4 = Myr_PI_Ms_1_4*R + Myd_PI_Ms_1_4*D;
    X1=step(Y_PI_Ms_1_4,t);
    X1=X1+operationPoint;
end

%% PI 2.0 Ms
if PI_Ms_2_0_enable
    Y_PI_Ms_2_0 = Myr_PI_Ms_2_0*R + Myd_PI_Ms_2_0*D;
    X2=step(Y_PI_Ms_2_0,t);
    X2=X2+operationPoint;
end

%% PID ODoL 1.4 Ms
if PID_Ms_1_4_enable
    Y_PID_Ms_1_4 = Myr_PID_Ms_1_4*R + Myd_PID_Ms_1_4*D;
    X3=step(Y_PID_Ms_1_4,t);
    X3=X3+operationPoint;
end

%% PID ODoL 2.0 Ms
if PID_Ms_2_0_enable
    Y_PID_Ms_2_0 = Myr_PID_Ms_2_0*R + Myd_PID_Ms_2_0*D;
    X4=step(Y_PID_Ms_2_0,t);
    X4=X4+operationPoint;
end

R=(t>TREF)*k_Ref;
R=R+operationPoint;
D=(t>TPER)*k_Per;
D=D+operationPoint;
