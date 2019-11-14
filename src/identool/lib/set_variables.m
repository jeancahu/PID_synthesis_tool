file_id = fopen(output_path+"identool_results.m", "wt");
file_json_id = fopen(output_path+"identool_results_json_format.txt", "wt");

%% Global variables definition
global To vo Lo Ko ynorm unorm tnorm long tin tmax tu

%% Load data from thread cache
carga=load(output_path+"step_response.txt"); % step response .txt load data
t=carga(:,1);                                % time vector
u=carga(:,2);                                % control signal vector
y=carga(:,3);                                % controled variable vector
long=length(t);                              % define the default length

% Infer vectors
diff_t = diff(t);
diff_u = diff(u);
diff_y = diff(y);

mean(diff_t(1:long/3))
mean(diff_u(1:long/3))
mean(diff_y(1:long/3))