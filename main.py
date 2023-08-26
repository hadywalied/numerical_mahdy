import itertools
import math
import os.path
import re
import subprocess

import pandas as pd


def main_loop(c, phi, x, base_):
    base_folder = os.path.join(os.getcwd(), f'run_c_{c}_phi_{phi}_x_{x}')
    os.makedirs(base_folder, exist_ok=True)

    input_file = os.path.join(base_folder, 'Slope_input.g2x')
    output_file = os.path.join(base_folder, 'Slope_output.g2x')
    log_file = os.path.join(base_folder, 'Slope_log.txt')
    X = 10 / math.tan(x * (math.pi / 180))
    with open(base_, 'r') as fd:
        file_lines = fd.read()
        file_lines = file_lines.replace("$Slope_X_top$", str(X))
        file_lines = file_lines.replace("$c$", str(c))
        file_lines = file_lines.replace("$Phi$", str(phi))

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
    base_file = 'Slope_Base.g2x'

    c_df = range(0, 21, 2)
    phi_df = range(20, 26, 1)
    x_df = range(10, 31, 10)
    p = [c_df, phi_df, x_df]
    possible_combinations = list(itertools.product(*p))

    result = pd.DataFrame(columns=['c', 'phi', 'beta', 'sf'])
    for i, combination in enumerate(possible_combinations):
        sf = main_loop(combination[0], combination[1], combination[2], base_file)
        result.loc[-1] = [combination[0], combination[1], combination[2], sf]
        result.index = result.index + 1
        result = result.sort_index()

    print(result)