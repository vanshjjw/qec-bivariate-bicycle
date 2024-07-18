import numpy as np
import subprocess
import re

def convert_to_gap_mat(mat):
        mat = np.array(mat,dtype=int)
        n_rows, n_cols = mat.shape
        mat_str = [','.join(map(str, row)) for row in mat]
        mat_str = '],\n['.join(mat_str)
        gap_code = "M := [".format(n_rows,n_cols) + "[" + mat_str + "]];;\n"
        return gap_code


def define_commands():
    commands = "LoadPackage(\"guava\");;"
    return commands


def definecode(h):
    commands= define_commands()

    # start_time = time.time()
    process = subprocess.Popen(['gap'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    std_output, std_error = process.communicate(commands)

    # Remove the special characters from gap's output like colours etc so you can search through it
    # ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # stdout=ansi_escape.sub('', stdout)
    # stdout=stdout.strip().replace(" ", "")

    return std_output


definecode([[1,1,0,0],[0,0,1,1]])
