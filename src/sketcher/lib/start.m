% Run on execution start

fprintf("Running initial module\n")

%clc;
clear;

%% Define
s=tf('s');
a=0.1; % Filter constant
action=1; % Inverse
operationPoint=50; % Working magnitude

% PID ODoF config
beta=1;
gamma=0;

% CRONE Oustaloup W-range
wl=0.001;
wh=1000;

% Simulation
k_Ref=15; % Rs intensity
k_Per=5; % Ds intensity
