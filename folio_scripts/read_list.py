#++++++++++++++++++++++++++
#
# TITLE: read_list
#
# PURPOSE: program reads in a list of data columns and
#          returns a dictionary  with the data in it.
#
# INPUTS: list_name: name of the file listing data
#         format_string: string giving the data type of each column
#         data_dir:  the directory where all the data
#                    will be created
#         delimiter: string that is used to separate data, defualt is
#                    whitespace
# OUTPUTS: returns a dictionary of the data with
#          string keys determined by the first line
#
# PROGRAM CALLS: NONE
#
# NOTES:
#        1. Data MUST be whitespace separated by default
#           set 'delimiter' to change this
#        2. Leading commented lines must start with '#'
#        3. First row following comments MUST be column names UNLESS
#           the column names are provided by the user
#        4. Data can be defined as I for integer data
#           F for float data, A for string data and format
#           string must be comma separated
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 4 JAN 2011
#
#-----------------------------------

def read_list(filename, format_string, delimiter = '', column_names = ''):
    # open file and skip any leading commented lines
    infile = open(filename)
    
    # if column names are not provided, read column names
    if column_names == '':
        while 1:
            columns = infile.readline()
            if columns[0] != '#':
                break
        columns = columns.strip()
        if delimiter != '':
            col_names = columns.split(delimiter)
        else:
            col_names = columns.split()
    else:
        col_names = column_names
        
    # remove commas in format string
    format_string = format_string.split(',')
    
    # now make sure that the number of columns is greater than
    # or equal to the number of format characters 
    if len(format_string) > len(col_names):
        print '---------------------------------------\n',
        print '       ERROR READING FILE:\n',
        print 'CHECK YOUR FILE AND FORMAT STRING!!!!\n',
        print 'format string has %d columns' %(len(format_string))
        print 'file has %d columns' %(len(col_names))
        print '---------------------------------------\n'
        return {}
    else:
        #build the dictionary
        data = {}
        good_col = []
        for count in range(len(format_string)):
            if format_string[count] != 'X':
                data[col_names[count]] = []
                good_col.append(count)
        for line in infile.readlines():
            if line[0] != '#':
                line = line.strip()
                if delimiter != '':
                    split_line = line.split(delimiter)
                else:
                    split_line = line.split()
                for index in good_col:
                    if format_string[index] == 'F':
                        if split_line[index] == 'null':
                            data[col_names[index]].append(float(-99.0))
                        else:
                            data[col_names[index]].append(float(split_line[index]))
                    elif format_string[index] == 'I':
                        if split_line[index] == 'null':
                            data[col_names[index]].append(int(-99.0))
                        else:
                            data[col_names[index]].append(int(split_line[index]))
                    elif format_string[index] == 'A':
                        data[col_names[index]].append(split_line[index])
    return data

        
