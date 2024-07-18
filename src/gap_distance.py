import subprocess
import numpy as np
def convert_to_gap_mat(mat1, mat2):
        mat1 = np.array(mat1,dtype=int)
        n_rows1, n_cols1 = mat1.shape
        mat_str1 = [','.join(map(str, row)) for row in mat1]
        mat_str1 = '],\n['.join(mat_str1)
        gap_code1 = "Hx := [".format(n_rows1,n_cols1) + "[" + mat_str1 + "]];;\n"
        mat2 = np.array(mat2,dtype=int)
        n_rows2, n_cols2 = mat2.shape
        mat_str2 = [','.join(map(str, row)) for row in mat2]
        mat_str2 = '],\n['.join(mat_str2)
        gap_code2 = "Hz := [".format(n_rows2,n_cols2) + "[" + mat_str2 + "]];;\n"
        gap_code=gap_code1+gap_code2
        return gap_code


def define_commands(H_x, H_z):
    commands = 'LoadPackage("guava");; LoadPackage("QDistRnd");;'+convert_to_gap_mat(H_x, H_z)+'F:=GF(2);; Hx:=One(F)*Hx;; Hz:=One(F)*Hz;;d:=DistRandCSS(Hz,Hx,100,0,2 : field:=F);'
    return commands


def definecode(H_x, H_z):
    commands= define_commands(H_x, H_z)

    # start_time = time.time()
    process = subprocess.Popen(['gap'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    std_output, std_error = process.communicate(commands)

    # Remove the special characters from gap's output like colours etc so you can search through it
    # ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # stdout=ansi_escape.sub('', stdout)
    # stdout=stdout.strip().replace(" ", "")
    return std_output, std_error