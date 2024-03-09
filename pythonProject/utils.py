import os
import sys
import shutil
import uuid
import subprocess
import urllib.request
import math
import random

def list_directory(dir_name):
    filenames = os.listdir(dir_name)
    return filenames


def list_directory_cmd(dir_name):
    cmd = 'dir ' + dir_name
    (status, output) = subprocess.getstatusoutput(cmd)
    return (status, output)

def get_web_page(url):
    # uf = urllib.request.urlopen(url)
    # uf.read()
    urllib.request.urlretrieve(url, str(uuid.uuid4()) + '.html')

def cat_file(filename):
    try:
        f = open(filename, 'rU')  # U ignores DOS/Unix line endings
        lines = []
        for line in f:
            lines.append(line)
        return lines
    except IOError:
        print( "IO Error", filename)
        return None


def cat_filename_2(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    return lines


def copy_file(file_name_src, file_name_des):
    shutil.copy(file_name_src, file_name_des)


def main():
    arg2 = sys.argv[2]
    d_name = sys.argv[1]
    f_name = os.path.join(os.getcwd(), arg2)
    if not os.path.isfile(f_name):
        raise Exception('invalid file name (argument 2)')
    if not os.path.exists(d_name):
        raise Exception('invalid directory name (argument 1)')
    print('contents of - ' + d_name)
    # print(list_directory(d_name))
    (status, output) = list_directory_cmd(d_name)
    if status:
        sys.stderr.write('there was an error:' + output)
        sys.exit(1)
    print(output)
    f_ext_index = arg2.rfind('.')
    f_ext = '' if f_ext_index == -1 else arg2[f_ext_index:]
    print('contents of - ' + f_name)
    print(''.join(cat_filename_2(f_name)))
    c_file_name = os.path.join(os.getcwd(), str(uuid.uuid4()) + f_ext)
    copy_file(f_name, c_file_name)
    print('copied to file - ' + c_file_name)

def grid_values(sudokuBoardStr, boxes):
    """Convert sudokuBoardStr string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    assert len(sudokuBoardStr) == 81
    return dict(zip(boxes, sudokuBoardStr))

def display(values, squares, rows, cols):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print (''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print( line)
    print

if __name__ == '__main__':
    main()
