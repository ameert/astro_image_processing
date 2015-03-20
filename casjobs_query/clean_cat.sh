#!/bin/bash

#list your input and output files

infile='./infile.txt'
outfile='./outfile.txt'

echo "#NOTE: null values have been replaced by -888" > ${outfile};

sed "s/null/-888/g" ${infile} >> ${outfile}; 
