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
mid_line_v1 = abs((in_v1(end)-in_v1(1))/2);
mid_line_v2 = abs((in_v2(end)-in_v2(1))/2);
mid_line_v3 = abs((in_v3(end)-in_v3(1))/2);

diff_v1 = diff(in_v1(m_long:end))/mid_line_v1;
diff_v2 = diff(in_v2(m_long:end))/mid_line_v2;
diff_v3 = diff(in_v3(m_long:end))/mid_line_v3;

mean_v1 = mean(abs(diff_v1));
mean_v2 = mean(abs(diff_v2));
mean_v3 = mean(abs(diff_v3));

%% Find u(s) in signals columns
u_v1=false;
u_v2=false;
u_v3=false;

if max(diff_v1) < mean_v2 && max(diff_v1) < mean_v3
    fprintf('\tu(s) is vector 1\n');
    u_v1=true;
    u = in_v1;
elseif max(diff_v2) < mean_v1 && max(diff_v2) < mean_v3
    fprintf('\tu(s) is vector 2\n');
    u_v2=true;
    u = in_v2;
else
    fprintf('\tu(s) is vector 3\n');
    u_v3=true;
    u = in_v3;
end

%% Find t(s) in signals columns
t_v1=false;
t_v2=false;
t_v3=false;

if ~u_v1 && min(diff_v1) > min(diff_v2) && min(diff_v1) > min(diff_v3)
    fprintf('\tt(s) is vector 1\n');
    t_v1=true;
    t = in_v1;
elseif ~u_v2 && min(diff_v2) > min(diff_v1) && min(diff_v2) > min(diff_v3)
    fprintf('\tt(s) is vector 2\n');
    t_v2=true;
    t = in_v2;
else
    fprintf('\tt(s) is vector 3\n');
    t_v3=true;
    t = in_v3;
end

%% Find y(s) in signals columns

if ~u_v1 && ~t_v1
    fprintf('\ty(s) is vector 1\n');
    y = in_v1;
elseif ~u_v2 && ~t_v2
    fprintf('\ty(s) is vector 2\n');
    y = in_v2;
else
    fprintf('\ty(s) is vector 3\n');
    y = in_v3;
end

%% FIXME, fixed definitions
t = in_v1;
u = in_v2;
y = in_v3;