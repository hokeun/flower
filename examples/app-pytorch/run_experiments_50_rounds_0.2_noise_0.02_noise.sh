#!/bin/bash

# Make sure to run poetry shell first!

date_time=$(date '+%Y_%m_%d_%H%M%S');

# Noise 0.2 sigma

HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.2_NOISE_0_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.2_NOISE_1_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.2_NOISE_2_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.2_NOISE_3_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.2_NOISE_4_TRIAL.txt



HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.2_NOISE_0_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.2_NOISE_1_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.2_NOISE_2_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.2_NOISE_3_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.2_NOISE_4_TRIAL.txt


HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.2_NOISE_0_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.2_NOISE_1_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.2_NOISE_2_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.2_NOISE_3_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.2 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.2_NOISE_4_TRIAL.txt

# Noise 0.02 sigma

HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.02_NOISE_0_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.02_NOISE_1_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.02_NOISE_2_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.02_NOISE_3_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_50_R_5_C_0.02_NOISE_4_TRIAL.txt



HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.02_NOISE_0_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.02_NOISE_1_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.02_NOISE_2_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.02_NOISE_3_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_50_R_10_C_0.02_NOISE_4_TRIAL.txt



HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.02_NOISE_0_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.02_NOISE_1_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.02_NOISE_2_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.02_NOISE_3_TRIAL.txt
HOKEUN_FLWR_NUM_ROUNDS=50 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.02 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 20' 2>&1 | tee "$date_time"_results_50_R_20_C_0.02_NOISE_4_TRIAL.txt