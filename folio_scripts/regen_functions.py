import numpy as np
import pyfits as pf
import sys

def load_G_file(filename):
    a = open(filename)
    b = a.read()
    a.close()
    
    return b

def replace_stamp(file_str, new_stamp):
    a = split_and_insert(file_str, 'A) ', new_stamp)
    return a

def replace_outfile(file_str, new_stamp):
    a = split_and_insert(file_str, 'B) ', new_stamp)
    return a

def replace_weight(file_str, new_stamp):
    a = split_and_insert(file_str, 'C) ', new_stamp)
    return a

def replace_psf(file_str, new_stamp):
    a = split_and_insert(file_str, 'D) ', new_stamp)
    return a

def replace_mask(file_str, new_stamp):
    a = split_and_insert(file_str, 'F) ', new_stamp)
    return a

def replace_constraints(file_str, new_stamp):
    a = split_and_insert(file_str, 'G) ', new_stamp)
    return a

def split_and_insert(input_str, start_str, new_str):
    str_parts = input_str.split(start_str)
    split_lines = str_parts[1]
    split_lines = split_lines.split('\n')
    split_mainline = split_lines[0].split()
    split_mainline[0] = new_str
    split_mainline = ' '.join(split_mainline)
    split_lines[0] = split_mainline
    split_lines = '\n'.join(split_lines)
    str_parts[1] = split_lines
    input_str = start_str.join(str_parts)
    return input_str

def fix_params(file_str):
    if ' 1 1 ' in file_str:
        file_str = file_str.replace(' 1 1 ', ' 0 0 ')
    tmp_split = file_str.split('# Object number:')
    for chunk_count, chunk in enumerate(tmp_split[1:]):
        tmp_split[chunk_count +1] = chunk.replace('  1  ', '  0  ')
    file_str = '# Object number:'.join(tmp_split)
    return file_str

def remake_G_file(infile, outfile, new_stamp, new_outfile, new_weight, new_psf, 
                  new_mask, new_constraints, fix_constraints = True):
    file_str = load_G_file(infile)

    if new_stamp != "NO_CHANGE":
        file_str = replace_stamp(file_str, new_stamp)
    if new_outfile != "NO_CHANGE":
        file_str = replace_outfile(file_str, new_outfile)
    if new_weight != "NO_CHANGE":
        file_str = replace_weight(file_str, new_weight)
    if new_psf != "NO_CHANGE":
        file_str = replace_psf(file_str, new_psf)
    if new_mask != "NO_CHANGE":
        file_str = replace_mask(file_str, new_mask)
    if new_constraints != "NO_CHANGE":
        file_str = replace_constraints(file_str, new_constraints)

    if fix_constraints:
        file_str = fix_params(file_str)
    
    a = open(outfile, 'w')
    a.write(file_str)
    a.close()

    return


