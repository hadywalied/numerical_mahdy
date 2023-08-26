import re
import subprocess

if __name__ == '__main__':
    input_file = 'Slope_Base.g2x'
    output_file = 'Slope_output.g2x'
    log_file = 'Slope_log.g2x'
    with open(input_file, 'r') as fd:
        file_lines = fd.read()
        file_lines = file_lines.replace("$X$", "10")

    with open(output_file, 'w') as fd:
        fd.write(file_lines)

    command = ['optumg2cmd', input_file, f'/output:{output_file}', f'/log:{log_file}', '/echo']

    p = subprocess.Popen(command, shell=True)
    p.wait()

    with open(log_file, 'r') as fd:
        lines = fd.read()
        rx1 = re.compile(r'BEST STRENGTH REDUCTION FACTOR = \d+\.\d+', re.IGNORECASE)
        rx2 = re.compile(r'\d+\.\d+', re.IGNORECASE)
        print(rx2.findall(rx1.findall(lines)[0])[0])
