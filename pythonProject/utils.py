import os
import sys
import math
import random


def list_directory(dir_name):
    filenames = os.listdir(dir_name)
    return filenames


def cat_file(filename):
    f = open(filename, 'rU')  # U ignores DOS/Unix line endings
    lines = []
    for line in f:
        lines.append(line)
    return lines


def cat_filename_2(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    return lines


def main():
    d_name = sys.argv[1]
    print('contents of - ' + d_name)
    print(list_directory(d_name))
    f_name = os.getcwd() + '\\' + sys.argv[2]
    print('contents of - ' + f_name)
    print(''.join(cat_filename_2(f_name)))


if __name__ == '__main__':
    main()
