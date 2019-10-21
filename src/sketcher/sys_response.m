%% Definicion de la salida, y perturbaciones:

%% PI 1.4 Ms
if PI_Ms_1_4_enable
    [X1_kref, X1_tref] = step(Myr_PI_Ms_1_4*k_Ref);
    [X1_kper, X1_tper] = step(Myd_PI_Ms_1_4*k_Per);
    X1=[X1_kref; (X1_kper + X1_kref(end))];
    X1=X1+operationPoint;
else
    X1=[0; 0];
    X1_tref=[0];
    X1_tper=[0];
end

%% PI 2.0 Ms
if PI_Ms_2_0_enable
    [X2_kref, X2_tref] = step(Myr_PI_Ms_2_0*k_Ref);
    [X2_kper, X2_tper] = step(Myd_PI_Ms_2_0*k_Per);
    X2=[X2_kref; (X2_kper + X2_kref(end))];
    X2=X2+operationPoint;
else
    X2=[0; 0];
    X2_tref=[0];
    X2_tper=[0];
end

%% PID ODoL 1.4 Ms
if PID_Ms_1_4_enable
    [X3_kref, X3_tref] = step(Myr_PID_Ms_1_4*k_Ref);
    [X3_kper, X3_tper] = step(Myd_PID_Ms_1_4*k_Per);
    X3=[X3_kref; (X3_kper + X3_kref(end))];
    X3=X3+operationPoint;
else
    X3=[0; 0];
    X3_tref=[0];
    X3_tper=[0];
end

%% PID ODoL 2.0 Ms
if PID_Ms_2_0_enable
    [X4_kref, X4_tref] = step(Myr_PID_Ms_2_0*k_Ref);
    [X4_kper, X4_tper] = step(Myd_PID_Ms_2_0*k_Per);
    X4=[X4_kref; (X4_kper + X4_kref(end))];
    X4=X4+operationPoint;
else
    X4=[0; 0];
    X4_tref=[0];
    X4_tper=[0];
end

% tiempo en que ocurre R
TREF=0;

% tiempo en que ocurre D FIXME
TPER=max([max(X1_tref) max(X2_tref) max(X3_tref) max(X4_tref)])*1.01;

X1_t = [X1_tref; (X1_tper + TPER)];
X2_t = [X2_tref; (X2_tper + TPER)];
X3_t = [X3_tref; (X3_tper + TPER)];
X4_t = [X4_tref; (X4_tper + TPER)];

TMAX=max([max(X1_t) max(X2_t) max(X3_t) max(X4_t)]);

t = [0; 0; TPER; TPER; TMAX]; % Default time vector

R=[0; k_Ref; k_Ref; k_Ref; k_Ref];
R=R+operationPoint;
D=[0; 0; 0; k_Per; k_Per];
D=D+operationPoint;

out = [t R];
savename=output_path+'R.txt';
save(savename,'out');

out = [t D];
savename=output_path+'D.txt';
save(savename,'out');

out = [X1_t X1];
savename=output_path+'R.txt';
save(savename,'out');

out = [X2_t X2];
savename=output_path+'R.txt';
save(savename,'out');

out = [X3_t X3];
savename=output_path+'R.txt';
save(savename,'out');

out = [X4_t X4];
savename=output_path+'R.txt';
save(savename,'out');

file_id = fopen(output_path+"ready.txt", "wt");
fprintf(file_id,'simulations_vectors_ready\n')
fclose(file_id);
