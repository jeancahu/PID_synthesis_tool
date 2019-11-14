file_id = fopen(output_path+"identool_results.m", "wt");
file_json_id = fopen(output_path+"identool_results_json_format.txt", "wt");

%% Global variables definition
global To vo Lo Ko ynorm unorm tnorm long tin tmax tu

%% Load data from thread cache
carga=load(output_path+"step_response.txt"); % step response .txt load data
in_v1=carga(:,1);                                % time vector
in_v2=carga(:,2);                                % control signal vector
in_v3=carga(:,3);                                % controled variable vector
long=length(in_v3);                              % define the default length
m_long=floor(long/2);

%% Infer vectors
diff_v1 = diff(in_v1);
diff_v2 = diff(in_v2);
diff_v3 = diff(in_v3);

sum_v1 = mean(abs(diff_v1(m_long:end)))*m_long;
sum_v2 = mean(abs(diff_v2(m_long:end)))*m_long;
sum_v3 = mean(abs(diff_v3(m_long:end)))*m_long;

mid_line_v1 = (in_v1(end)-in_v1(1))/2;
mid_line_v2 = (in_v2(end)-in_v2(1))/2;
mid_line_v3 = (in_v3(end)-in_v3(1))/2;

in_v1_index = abs(sum_v1/mid_line_v1)
in_v2_index = abs(sum_v2/mid_line_v2)
in_v3_index = abs(sum_v3/mid_line_v3)

t = in_v1;
u = in_v2;
y = in_v3;