#!/usr/bin/env python3

import argparse
import os

from enum import Enum
import re

class SummaryState(Enum):
    NONE = 1
    TRAIN_ACCURACY = 2
    TRAIN_LOSS = 3
    VAL_ACCURACY = 4
    VAL_LOSS = 5

class Summary:
    def __init__(self):
        self.file_name = ""
        self.trial_count = 0
        self.num_clients = 0
        self.num_rounds = 0
        self.noise_enabled = False
        self.gauss_noise_sigma = 0.0
        self.param_count = 0
        self.mult_count = 0
        self.train_accuracy = []
        self.train_loss = []
        self.val_accuracy = []
        self.val_loss = []

    def __str__(self):
        return f"""----------------------
file_name: {self.file_name}
trial_count: {self.trial_count}
num_clients: {self.num_clients}
num_rounds: {self.num_rounds}
noise_enabled: {self.noise_enabled}
gauss_noise_sigma: {self.gauss_noise_sigma}
param_count: {self.param_count}
mult_count: {self.mult_count}
train_accuracy: {self.train_accuracy}

train_loss: {self.train_loss}

val_accuracy: {self.val_accuracy}

val_loss: {self.val_loss}
----------------------"""


def get_summary(file_path: str):
    result_file = open(file_path, 'r')
    result_lines = result_file.readlines()

    state = SummaryState.NONE

    summary = Summary()

    summary.file_name = os.path.basename(file_path)
    summary.trial_count = int(re.search("_(?P<count>[0-9]+)_TRIAL", summary.file_name).group("count"))

    for line in result_lines:
        if state == SummaryState.NONE:
            if "'train_accuracy'" in line:
                state = SummaryState.TRAIN_ACCURACY
            if "'train_loss'" in line:
                state = SummaryState.TRAIN_LOSS
            if "'val_accuracy'" in line:
                state = SummaryState.VAL_ACCURACY
            if "'val_loss'" in line:
                state = SummaryState.VAL_LOSS

        if state == SummaryState.NONE:
            tokens = line.split(":")
            if "configure_fit: strategy sampled" in line:
                summary.num_clients = int(re.search("sampled (?P<count>[0-9]+) clients", line).group("count"))
            if "env_var_num_rounds:" in line:
                summary.num_rounds = int(tokens[-1])
            if "aggregate_inplace: noise_enabled:" in line:
                summary.noise_enabled = tokens[-1] == "True"
            if "aggregate_inplace: gauss_noise_sigma:" in line:
                summary.gauss_noise_sigma = float(tokens[-1])
            if "aggregate_inplace: hokeun_deep_count_float32(params):" in line:
                summary.param_count = int(tokens[-1])
            if "aggregate_inplace: mult_count:" in line:
                summary.mult_count = int(tokens[-1])

        # Get data
        if state != SummaryState.NONE:
            tuple_str = re.findall(r"\(.*?\)", line)
            tuple_str = re.sub("[()]", "", tuple_str[0])
            tuple = [x.strip() for x in tuple_str.split(",")]
            tuple = [int(tuple[0]), float(tuple[1])]

            if state == SummaryState.TRAIN_ACCURACY:
                summary.train_accuracy.append(tuple)
            if state == SummaryState.TRAIN_LOSS:
                summary.train_loss.append(tuple)
            if state == SummaryState.VAL_ACCURACY:
                summary.val_accuracy.append(tuple)
            if state == SummaryState.VAL_LOSS:
                summary.val_loss.append(tuple)

            if "]" in line:
                state = SummaryState.NONE
    
    return summary

    # print("Hokeun! train_accuracy: ", summary.train_accuracy)
    # print("Hokeun! train_loss: ", summary.train_loss)
    # print("Hokeun! val_accuracy: ", summary.val_accuracy)
    # print("Hokeun! val_loss: ", summary.val_loss)
        # count += 1
        # print("Line {}: {}".format(count, line.strip()))
        # if count > 10:
        #     break


parser = argparse.ArgumentParser(description = "Summarize experimental results in directory.")

parser.add_argument("-d", "--dir",
                    required = True, dest ="target_dir", 
                    action = "store", 
                    help = "The directory including the experimental result files.")

args = parser.parse_args()

file_list = os.listdir(args.target_dir)
file_list.sort()
# print("Hokeun! " + str(file_list))

print("num_clients\tgauss_noise_sigma\ttrial_count\ttrain_accuracy\tval_accuracy")
for file in file_list:
    summary = get_summary(os.path.join(args.target_dir, file))
    # print(summary) # For debugging.
    print(f"{summary.num_clients}\t{summary.gauss_noise_sigma}\t{summary.trial_count}\t{summary.train_accuracy[-1][1]}\t{summary.val_accuracy[-1][1]}")