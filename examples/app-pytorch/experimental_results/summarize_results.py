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

def get_summary(file_path: str):
    result_file = open(file_path, 'r')
    result_lines = result_file.readlines()

    train_accuracy = []
    train_loss = []
    val_accuracy = []
    val_loss = []

    state = SummaryState.NONE

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

        # Get data
        if state != SummaryState.NONE:
            tuple_str = re.findall(r"\(.*?\)", line)
            tuple_str = re.sub("[()]", "", tuple_str[0])
            tuple = [x.strip() for x in tuple_str.split(",")]
            tuple = [int(tuple[0]), float(tuple[1])]

            if state == SummaryState.TRAIN_ACCURACY:
                train_accuracy.append(tuple)
            if state == SummaryState.TRAIN_LOSS:
                train_loss.append(tuple)
            if state == SummaryState.VAL_ACCURACY:
                val_accuracy.append(tuple)
            if state == SummaryState.VAL_LOSS:
                val_loss.append(tuple)

            if "]" in line:
                state = SummaryState.NONE
    

    # print("Hokeun! train_accuracy: ", train_accuracy)
    # print("Hokeun! train_loss: ", train_loss)
    # print("Hokeun! val_accuracy: ", val_accuracy)
    # print("Hokeun! val_loss: ", val_loss)
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
print("Hokeun! " + str(file_list))

get_summary(os.path.join(args.target_dir, file_list[0]))