#!/bin/bash

# Make sure to run poetry shell first!

date_time=$(date '+%Y_%m_%d_%H%M%S');

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=0 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.0 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_20_R_5_C_0_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=1.0 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_20_R_5_C_1.0_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.5 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_20_R_5_C_0.5_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.1 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_20_R_5_C_0.1_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.05 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_20_R_5_C_0.05_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.01 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 5' 2>&1 | tee "$date_time"_results_20_R_5_C_0.01_NOISE.txt





HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=0 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.0 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_20_R_10_C_0_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=1.0 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_20_R_10_C_1.0_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.5 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_20_R_10_C_0.5_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.1 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_20_R_10_C_0.1_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.05 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_20_R_10_C_0.05_NOISE.txt

HOKEUN_FLWR_NUM_ROUNDS=20 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.01 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 10' 2>&1 | tee "$date_time"_results_20_R_10_C_0.01_NOISE.txt

