import itertools
import math
import os.path
import re
import subprocess

import pandas as pd


def main_loop(H, B, q, R_int, gamma, Su, base_, i):
    base_folder = os.path.join(os.getcwd(), 'out', f'run_{i}_{base_}')
    os.makedirs(base_folder, exist_ok=True)

    input_file = os.path.join(base_folder, 'Slope_input.g2x')
    output_file = os.path.join(base_folder, 'Slope_output.g2x')
    log_file = os.path.join(base_folder, 'Slope_log.txt')

    with open(base_, 'r') as fd:
        file_lines = fd.read()
        file_lines = file_lines.replace("$H$", str(-H))
        file_lines = file_lines.replace("$B$", str(-B))
        file_lines = file_lines.replace("$q$", str(-q))
        file_lines = file_lines.replace("$Rint$", str(R_int))
        file_lines = file_lines.replace("$gamma$", str(gamma))
        file_lines = file_lines.replace("$Su$", str(Su))


    with open(input_file, 'w+') as fd:
        fd.write(file_lines)

    command = ['optumg2cmd', input_file, f'/output:{output_file}', f'/log:{log_file}', '/echo']
    p = subprocess.Popen(command, shell=True)
    p.wait()

    with open(log_file, 'r') as fd:
        lines = fd.read()
        rx1 = re.compile(r'BEST STRENGTH REDUCTION FACTOR = \d+\.\d+', re.IGNORECASE)
        rx2 = re.compile(r'\d+\.\d+', re.IGNORECASE)
        return rx2.findall(rx1.findall(lines)[0])[0]


if __name__ == '__main__':
    base_file_lower = 'Base_Model_Param_lower.g2x'
    base_file_upper = 'Base_Model_Param_upper.g2x'
    output_csv_file = 'output_results.csv'

    H = range(2, 13, 2)
    B = range(2, 13, 2)
    q = range(0, 51, 10)
    R_int = [0.6, 0.8, 1.0]
    gamma = range(14, 21, 1)
    s_u = [25, 50, 75, 100, 150]

    p = [H, B, q, R_int, gamma, s_u]
    possible_combinations = list(itertools.product(*p))

    result = pd.DataFrame(columns=['H', 'B', 'q', 'R_int', 'gamma', 'Su', 'sf_lower', 'sf_upper'])
    for i, combination in enumerate(possible_combinations):
        sf_l = main_loop(*combination, base_file_lower, i)
        sf_u = main_loop(*combination, base_file_upper, i)

        result.loc[-1] = [*combination, sf_l, sf_u]
        result.index = result.index + 1
        result = result.sort_index()

        result.to_csv(output_csv_file)

    print(result)
