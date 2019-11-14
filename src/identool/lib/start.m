% Run on execution start

fprintf("Running initial module\n")

%clc;
clear;

%% Define
s=tf('s');

file_id = fopen(output_path+"identool_results.m", "wt");
file_json_id = fopen(output_path+"identool_results_json_format.txt", "wt");
