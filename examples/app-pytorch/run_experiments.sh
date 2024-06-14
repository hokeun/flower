#!/bin/bash

# Make sure to run poetry shell first!

date_time=$(date '+%Y_%m_%d_%H%M%S');

echo 
echo "========================================================="
echo 

HOKEUN_FLWR_NUM_ROUNDS=2 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.1 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 2' 2>&1 | tee "$date_time"_results_1.txt

echo 
echo "========================================================="
echo 

HOKEUN_FLWR_NUM_ROUNDS=2 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.1 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 2' 2>&1 | tee "$date_time"_results_2.txt

echo 
echo "========================================================="
echo 

