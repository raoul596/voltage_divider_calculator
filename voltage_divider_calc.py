#!/usr/bin/env python3

import numpy as np
from argparse import ArgumentParser

E24_VALUES = [10,11,12,13,15,16,18,20,22,24,27,30,33,36,39,43,47,51,56,62,68,75,82,91]

parser = ArgumentParser(description='Voltage divider calculator')
parser.add_argument("-s", "--source_voltage", dest="source_voltage", default=5000, help="The voltage supplied to both resistors (R1 & R2) in mV")
parser.add_argument("-o", "--output_voltage", dest="output_voltage", default=2500, help="The voltage over the bottom resistor R2 in mV")

args = parser.parse_args()

def find_closest_index(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    return idx

def exp(base, exp):
    return base * 10 ** exp

#1 10 100 1k 10k 100k 1M 10M
def calc_combinations(vout):
    for exponent_r1 in range(-1, 7):
        for r1 in E24_VALUES:
            for exponent_r2 in range(-1, 7):
                for r2 in E24_VALUES:
                    current_pair = "R1: " + str(exp(r1, exponent_r1)) + "  r2:" + str(exp(r2, exponent_r2))
                    vout[current_pair] = (int(args.source_voltage) * exp(r2, exponent_r2)) / (exp(r1, exponent_r1) + exp(r2, exponent_r2))
        
    return vout
    
def sort_dict(keys, values):
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

    return sorted_dict

def dict_to_list(dict):
    keys = list(dict.keys())
    values = list(dict.values())

    return keys, values

def main():
    vout = {}

    calc_combinations(vout)

    resistors, voltage = dict_to_list(vout)
    vout = sort_dict(resistors, voltage)
    resistors, voltage = dict_to_list(vout)

    closest_index = find_closest_index(voltage, int(args.output_voltage))

    table = [["", "previous closest", "closest", "next closest"], 
        ["values", resistors[closest_index-1], resistors[closest_index], resistors[closest_index+1]],
        ["voltage mV", round(voltage[closest_index-1],4), round(voltage[closest_index],4), round(voltage[closest_index+1],4)]]
   
    for row in table:
        print('| {:<10} | {:<16} | {:<16} | {:<16} |'.format(*row))

if __name__=="__main__":
    main()
