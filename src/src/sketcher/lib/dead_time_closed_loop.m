%%
%% Author: Ing. Jeancarlo Hidalgo U.
%%
%% Close-Loop System: Y(s) =       R(s)*A(s)*C(s)*Exp(-Ls))
%%                            --------------------------------
%%                                   1+C(s)*B(s)*Exp(-Ls)
%%
%%                 ____________                            ____________________
%%                 |          |                            |                  |
%%  R(s)-------->  |    A(s)  |  ------------>(+)--------> |   C(s)Exp(-Ls)   |  -----x---> Y(s)
%%                 |__________|                ^           |__________________|       v
%%                                             ^                                      v
%%                 ____________                ^                                      v
%%                 |          |                ^                                      v
%%         ^-----> |    B(s)  | ---------------^                                      v
%%         ^       |__________|                                                       v
%%         ^                                                                          v
%%         ^--------------------------------------------------------------------------v
%%

%% Open-Loop equivalent System:
%%
%%                 ____________                                 _____________
%%                 |          |                                 |           |
%%  R(s)-------->  |    A(s)  |  ------------>(+)-------------> |    C(s)   |  -----------> Y(n)
%%                 |__________|                ^                |___________|
%%                                             ^
%%                 ____________                ^
%%                 |          |                ^
%%  Y(n-1) ----->  |    B(s)  | ---------------^
%%                 |__________|
%%
%%
%%

% input_L: float, must be more than 0.1
% input_A: tf
% input_B: tf
% input_C: tf

function [yn_sum, local_step, local_time] = dead_time_closed_loop(input_A, input_B, input_C, input_L)
  s = tf("s");

  if (input_L < 0.1)
    error('Error.L must be more than 0.1')
  end

  %% Octave PADE delay approximation
  [pade_num, pade_den] = padecoef(input_L,2);
  pade_delay=tf(pade_num,pade_den);

  input_C_pade = input_C*pade_delay;

  local_Myr = input_A*input_C/(1+input_B*input_C);
  local_Myr_pade_delay = input_A*input_C_pade/(1+input_B*input_C_pade);

  [local_y_pade,local_time] =step(local_Myr_pade_delay);

  if ((input_L*100)/max(local_time)) %% L is less than 1% time simulation
    timestep_L_ratio=26.0;
  else
    timestep_L_ratio=double(int32((L*12000)/max(local_time))) %% Tries to aprox 12K simulations
  end
  local_time = [0:input_L/timestep_L_ratio:max(local_time)*1.1];
  local_y_pade = step(local_Myr_pade_delay,local_time);


  local_step = (local_time > max(local_time)*0.1); %% step at 10%
  local_step_delay_0 = (local_time > (max(local_time)*0.1+input_L)); %% step at 10%

  y_pade = lsim(local_Myr_pade_delay, local_step, local_time);

  y = lsim(local_Myr, local_step, local_time);


  y_temp = lsim(input_A*input_C, local_step_delay_0, local_time);
  yn_sum = y_temp; %% Sume all the signals together
  yn = [];

  delay_steps = [0:input_L:max(local_time)*1.1];
  for i = delay_steps %% Delay steps
    y_temp = lsim(input_B*input_C, y_temp, local_time);
    B = zeros(size(y_temp));
    B(timestep_L_ratio+1:end) = y_temp(1:length(y_temp) - timestep_L_ratio);
    y_temp = B;
    yn = [yn y_temp];
  end

  %% Use PADE for yn matrix > 49
  if (length(yn(1,:)) > 48)
    for i = [1:48]
      yn_sum = yn_sum + ((-1.0)^i)*yn(:,i);
    end
    yn_sum(int32(length(yn_sum)/2):end) = y_pade(int32(length(yn_sum)/2):end); %% Use PADE where it is accurate
  else
    %% Sum individual Yn to get Y(t)
    for i = [1:length(yn(1,:))] %% colums
      yn_sum = yn_sum + ((-1.0)^i)*yn(:,i);
    end
  end

                 %plot(local_time, yn_sum, local_time, local_step); %% y_sum
                 %plot(local_time, y_pade, local_time, local_step); %% Pade
end
