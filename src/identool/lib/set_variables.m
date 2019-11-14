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
m_long=long/2;

% Infer vectors
a_diff_t = abs(diff(t));
a_diff_u = abs(diff(u));
a_diff_y = abs(diff(y));

mean(a_diff_t(m_long:end))
mean(a_diff_u(m_long:end))
mean(a_diff_y(m_long:end))

sum(a_diff_t)
sum(a_diff_u)
sum(a_diff_y)