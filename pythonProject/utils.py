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


def test_sudoku_setup(squares, unitlist, units, peers):
    "A set of unit tests."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')

    
def parse_grid(grid, cells, units,peers):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    digits   = '123456789'
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in cells)
    for s,d in grid_values(grid, cells).items():
        if d in digits and not assign(values, s, d, units,peers):
            return False ## (Fail if we can't assign d to square s.)
    return values

def assign(values, s, d, units, peers):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2, units, peers) for d2 in other_values):
        return values
    else:
        return False
    
def eliminate(values, s, d, units,peers):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2, units, peers) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
                if not assign(values, dplaces[0], d, units, peers):
                    return False
    return values
