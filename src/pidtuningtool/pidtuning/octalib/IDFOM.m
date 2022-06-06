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
y = in_v3;%% Main execution
% The next program is able to generate the fractional model parameters
% compute previous variables and then get the final constants

fprintf('Optimal model is in process...\n')

%% Static gain processing
% Vectors in file need to keep same lenght
sample=7;                        % Get noise avernage value
Uo=mean(u(1:sample));            %
Uf=mean(u(long-sample+1:long));  %
Yo=mean(y(1:sample));            % Clean noise
Yf=mean(y(long-sample+1:long));
Ko=(Yf-Yo)/(Uf-Uo);              % Get controled process gain

% Parameters normalization

ynorm=(y-Yo)./(Yf-Yo);       % Controlled variable vector with normalized values
unorm=(u-Uo)./(Uf-Uo);       % Control signal vector with normalized values
tnorm=t-min(t);              % Normalized time vector
ymax=max(ynorm);             % Sampling from non zero 't'

% Get_step_time rutine
cont=1;
flagtin=0;
% Flag variable
while cont<long
    if unorm(cont+1)>unorm(cont) || unorm(cont+1)<unorm(cont)
        tin=tnorm(cont);
        flagtin=cont;        % Obtain the tin position in data vector
        cont=long;
    else
        cont=cont+1;
    end
end


%% Initial values computation
% Default data for initial iteration

m1=1; % Temporal variables define
while m1<long
    % Get position of point over 63.2% of yinf
    if ynorm(m1)>0.632*ynorm(long)
        t63=tnorm(m1); % Time when 'y' is 63.2% of max(y)
        y63=ynorm(m1);
        m1=long;
    else
        m1=m1+1;
    end
end

m2=1;
while m2<long
    % Get position of first point over 3% of yinf
    if ynorm(m2)>0.03*ynorm(long) && tnorm(m2)>tin
        t3=tnorm(m2); % Time when 'y' is 3% of max(y)
        y3=ynorm(m2);
        m2=long;
    else
        m2=m2+1;
    end
end

m3=1;
while m3<long
    % Get position of first point over 90% of yinf
    if ynorm(m3)>0.9*ynorm(long)
        t90=tnorm(m3); % Time when 'y' is 3% of max(y)
        y90=ynorm(m3);
        m3=long;
    else
        m3=m3+1;
    end
end

%% Fractional order initial value

v=0;
tt=t63/t90;

% Overshoot when dynamic underdamped
Mp=(ymax-ynorm(long))/ynorm(long);

% Obtain fractional order (v) from previous results
if (ymax>ynorm(long))
    syms v;
    v1 = (1.4182+sqrt((-1.4182)^2 - 4*0.8032*(0.6115-Mp))) / (2*0.8032);
    v2 = (1.4182-sqrt((-1.4182)^2 - 4*0.8032*(0.6115-Mp))) / (2*0.8032);
    if isreal(v1) && isreal(v2)
        if (v1>=1 && v1<=3)
            v0=v1;
        else
            v0=v2;
        end
    end
elseif (tt>=0 && tt<0.4325)
    p=1; tx2=zeros(1,71);
    for x=0.3:0.01:1 %variacion orden fraccional
        tx=-0.1621*x^3+0.9351*x^2+-0.4089*x+0.0711;
        tx2(p)=tx;
        p=p+1;
    end
    [row_a,col_a]=find(tx2>=tt,1,'first');
    v0=0.3+0.01*(col_a-1);
else
    v0=1;
end

% Obtain the times signal cross over 1
if v0>1.3 % Only compute this data when FT or MTE is introduced
    cont3=1;
    totalosc=0;
    while cont3<long
        if ynorm(cont3)<1 && ynorm(cont3+1)>1
            totalosc=totalosc+1;
            cont3=cont3+1;
        else
            cont3=cont3+1;
        end
    end
end

% L0 definition
L0=t3-tin;

%& Algorithm for L0 computation
% Get settling time
if v0>=1.1525
    ma=long;
    while ma>1
        if (ynorm(ma)>=1.05 || ynorm(ma)<=0.95)
            ta=tnorm(ma); % Settling time
            ya=ynorm(ma);
            ma=1;
        else
            ma=ma-1;
        end
    end
end

if v0>=1.4349 && totalosc>=2
    % Oscillation time
    os=1; % Oscillation time need to be greater than one
    while os<long
        if ynorm(os)>=1
            tu1=tnorm(os);
            yu1=ynorm(os);
            temp1=os;
            os=long;
        else
            os=os+1;
        end
    end

    os=temp1;
    while os<long
        if ynorm(os)<=1
            tu2=tnorm(os);
            yu2=ynorm(os);
            os=long;
        else
            os=os+1;
        end
    end

    tu=tu2-tu1; % Obtain half period

    %::::::::::::::Condiciones para la asignación de T0::::::::::
    diff=0.05;
    tuT0=0;
    while tuT0<tu
        [zT0 pT0 kT0] =APC(1, v0, 0.001, 1000);
        MT0=zpk(zT0,pT0,kT0);
        MMT0=1/(diff*MT0+1);
        [yT0,tT0]=step(MMT0,tnorm);
        longT0=length(yT0);

        % tuT0 calculation
        os=1;
        while os<longT0
            if yT0(os)>=1
                tu1T0=t(os);
                yu1T0=y(os);
                temp1=os;
                os=longT0;
            else
                os=os+1;
            end
        end

        os=temp1;
        while os<longT0
            if yT0(os)<=1
                tu2T0=t(os);
                yu2T0=y(os);
                os=longT0;
            else
                os=os+1;
            end
        end

        tuT0=tu2T0-tu1T0; % half period

        % Verify condition
        if tu<=tuT0
            T0=diff;     % T0 definition
        else
            diff=0.05+diff;
        end
    end

else
    T0=(t63-(tin+L0))^v0;
end

%% Get initial model form
fprintf("Computing initial model\n")

    % Model to use
    if v0<1
        [z0, p0, k0]=APC(1,-v0,0.001,1000);  % Approach
        Gmm=zpk(z0,p0,k0);
        Gmm=1/Gmm;
    else
        [z0, p0, k0]=APC(1,v0,0.001,1000);   % Approach
        Gmm=zpk(z0,p0,k0);
    end

    try
      if (version_info.Name=="MATLAB")
       Gm0 = 1*exp(-(L0+tin)*s)/(T0*Gmm+1);     % Define initial model for MATLAB
      end
    catch ME
      %% Octave PADE delay approximation
      [pade_num, pade_den] = padecoef(L0+tin,18);
      pade_delay=tf(pade_num,pade_den);
      Gm0 = pade_delay/(T0*Gmm+1);     % Define initial model
    end

    ym0=step(Gm0,tnorm);                     % set tolerances
    Tolf=trapz(tnorm,abs(ym0-ynorm))*1e-7;   % optimization (Tolx and Tolf).
    Tolx=norm([T0 v0 L0])*1e-7;

%::::::::::::::::::::Optimización:::::::::::::::::::::::::::

%se establecen las opciones para llevar a cabo la optiización
options = optimset('MaxIter', ...
                   200, ...
                   'MaxFunEvals', ...
                   1000, ...
                   'Algorithm', ...
                   'active-set', ...
                   'TolFun', ...
                   Tolf, ...
                   'TolX', ...
                   Tolx, ...
                   'Display', ...
                   'off');

x0 = [T0 v0 L0]; % Initial paramenters and optimization command with evaluation range
costfun = @(xns)f_IDFOM(xns, tnorm, ynorm, tin, flagtin, 1);

[xns,IAEns] = fmincon(costfun, ...
                      x0, ...
                      [], ...
                      [], ...
                      [], ...
                      [], ...
                      x0*(1-0.9), ...
                      x0*(1+0.9), ...
                      [], ...
                      options);

To=xns(1); % Time constant
vo=xns(2); % Fractional order
Lo=xns(3); % Dead time

% Model:
tmax=max(tnorm);
if vo<1
   [zo, po, koo]=APC(1,-vo,0.001,1000);
   Gm= 1/zpk(zo,po,koo);
else
    [zo, po, koo]=APC(1,vo,0.001,1000);
    Gm= zpk(zo,po,koo);
end

try
  if (version_info.Name=="MATLAB")
    Gmo=Ko*exp(-(Lo+tin)*s)/(To*Gm+1); % Define the tf for MATLAB
  end
catch ME
  %% Octave PADE delay approximation
  [pade_num, pade_den] = padecoef(Lo+tin,18);
  pade_delay=tf(pade_num,pade_den);
  Gmo=Ko*pade_delay/(To*Gm+1);
end

ym=step(Gmo,tnorm);

%% Print parameters
fprintf('Initial model paramenters:\n')
if (Ko/floor(Ko))~=1
    fprintf('  K\t= %4.2d\n',Ko)
else
    fprintf('  K\t= %4.1d\n',Ko)
end
if (Lo/floor(Lo))~=1
    fprintf('  L\t= %1.2d\n',Lo)
else
    fprintf('  L\t= %1.1d\n',Lo)
end
if vo==1
    fprintf('  v\t= %1.1d\n',vo)
else
    fprintf('  v\t= %1.2d\n',vo)
end
if (To/floor(To))~=1
    fprintf('  T\t= %1.2d\n',To)
else
    fprintf('  T\t= %1.1d\n',To)
end
fprintf('  IAE\t= %1.2d\n',IAEns)

fprintf('Fractional order model:\n')
fprintf('\t\t %1.2E*exp(-%1.2Es)\n',Ko,Lo)
fprintf('Gm(s)=\t----------------------------\n')
fprintf('\t\t\t%1.2Es^%1.2E+1 \n',To,vo)

%% Write optimal model in results cache file:
fprintf(file_json_id, '{\n');
fprintf(file_json_id, '\t"type": "fractional_model",\n');
fprintf(file_json_id, '\t"v": %.20f,\n', vo);
fprintf(file_json_id, '\t"T": %.20f,\n', To);
fprintf(file_json_id, '\t"K": %.20f,\n', Ko);
fprintf(file_json_id, '\t"L": %.20f,\n', Lo);
fprintf(file_json_id, '\t"IAE": %.20f\n', IAEns);
fprintf(file_json_id, '}\n');


%% Write optimal model in results cache file:
fprintf(file_id,'v=%.20f;',vo);
fprintf(file_id,'T=%.20f;',To);
fprintf(file_id,'K=%.20f;',Ko);
fprintf(file_id,'L=%.20f;',Lo);
fprintf(file_id,' %% model_calculated_values\n');

%% Graphics and simulations:
figure(1)
subplot(2,1,1)
  plot(tnorm,u,'g',tnorm,y,'b','LineWidth',1.2)
  grid on;
  ylabel('Signals magnitude (%)')
  xlabel('Time (s)')
  xlim([0 tmax])
  yu_min=min(min(y,u));
  yu_max=max(max(y,u));
  if yu_min<0
      ylim([1.1*yu_min 1.1*yu_max])
  else
      ylim([0.9*yu_min 1.1*yu_max])
  end
  legend('r(t)','y(t)','Location','East')
  title('Original input signals')

subplot(2,1,2)
  plot(tnorm,unorm,'g',tnorm,ynorm,'b',tnorm,ym/Ko,'r','LineWidth',1.2)
  grid on;
  ylabel('Signals magnitude (%)');
  xlabel('Time (s)');
  xlim([0 tmax]);
  if (min(ynorm)>=0)
      ylim([0.90*min(ynorm) 1.1*ymax])
  else
      ylim([1.1*min(ynorm) 1.1*ymax])
  end
  legend('r(t)','y(t)','y_m(t)','Location','East');
  title('Step response for optimal model');

% Save the image
print("./model_comparison.png",'-dpng')
fprintf('Image ready\n')

% Save signals to file
out = [tnorm unorm ynorm ym/Ko];
fid=fopen("./model_step_response.txt",'wt');
for i = 1:length(out)
    fprintf(fid,'%d\t%d\t%d\t%d\n',out(i,1),out(i,2),out(i,3),out(i,4));
end
fclose(fid);

file_flag_id = fopen("./ready.txt", "a+");
fprintf(file_flag_id,'model_comparison_ready\n');
fclose(file_flag_id);
fclose(file_id);
fclose(file_json_id);
