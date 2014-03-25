import os
import sys
import numpy as np


models = ['Test', 'SerExp', 'DevExp']

row1str = ' c '*len(models)
row2str = ["""\\textbf{{\% {modname}}}""".format(modname=modname) for modname in models]

row2str = ' & '.join(row2str)

indata = []

for mod in models:
    indat1 = np.loadtxt('%s_catalog.table' %mod, delimiter = ':', usecols = [1])
    indata.append(indat1)

indata = np.array(indata).T

outstr = ["""\\begin{tabular}{l l l l l %s}""",
"""\\textbf{Fit Type} & \\multicolumn{4}{l}{\\textbf{Descriptive Category}} &  %s \\\\ \\hline""",
""" & \\multicolumn{4}{l}{\\textbf{Trustable 2-com Total Fit}} & %s\\\\""",

"""1 & & \\multicolumn{3}{l}{\\textbf{Probable Single-Component Galaxies, Components OK}} & %s\\\\""",
"""2 & & & \\multicolumn{2}{l}{No \Ser} & %s\\\\""",
"""& & &\\multicolumn{2}{l}{No \Exp} & %s \\\\""",
"""3 & & & & Good \Ser, n$_{\Ser}>$2, No \Exp & %s\\\\""",
"""2 & & & & Good \Ser, n$_{\Ser}<$2, No \Exp, Flip Components & %s\\\\""",

"""4 & & \\multicolumn{3}{l}{\\textbf{Possible Two-Component Galaxies, Components OK}} & %s \\\\""",
""" & & & \\multicolumn{2}{l}{No Flags} & %s \\\\""",
""" & & &\\multicolumn{2}{l}{Good \Ser, Good \Exp\ (Some Flags)} & %s \\\\""",
""" & & &\\multicolumn{2}{l}{Good \Ser, Bad \Exp, B/T$>=$0.5} & %s \\\\""",
""" & & &\\multicolumn{2}{l}{Bad \Ser, Good \Exp, B/T$<$0.5} & %s \\\\""",
""" & & &\\multicolumn{2}{l}{Flip Components, Otherwise Good} & %s \\\\""",

"""1 & & \\multicolumn{3}{l}{\\textbf{Probable Single-Component Galaxies, Component Problems}} & %s\\\\""",
"""3 & & &  \\multicolumn{2}{l}{\Ser\ Dominates Always} & %s \\\\""",
"""2 & & & \\multicolumn{2}{l}{\Exp\ Dominates Always} & %s \\\\""",
"""2 & & & \\multicolumn{2}{l}{Parallel Components} & %s \\\\""",

"""4 & & \\multicolumn{3}{l}{\\textbf{Possible Two-Component Galaxies, Component Problems}} & %s \\\\""",
"""& & &\\multicolumn{2}{l}{\Ser\ Outer Only} & %s \\\\""",
"""& & &\\multicolumn{2}{l}{\Exp\ Inner Only} & %s \\\\""",
"""& & &\\multicolumn{2}{l}{Flip Components, and Bad Components} & %s \\\\""",
"""& & & \\multicolumn{2}{l}{Bad \Ser, Bad \Exp} & %s \\\\""",
"""5 & \\multicolumn{4}{l}{\\textbf{2-com Total Fit Problems}} & %s\\\\""",
"""& & \\multicolumn{3}{l}{\\textbf{Bad Total}} & %s \\\\""",
"""& & \\multicolumn{3}{l}{\\textbf{Galfit Failure}} & %s \\\\""",
"""\\end{tabular}"""
]

outstr[0] = outstr[0] %row1str
outstr[1] = outstr[1] %row2str

for rowcount, row in enumerate(indata):
    rowvals = ['%.3f' %a for a in row]
    rowvals = ' & '.join(rowvals)
    outstr[2+rowcount]= outstr[2+rowcount] %rowvals

outfile = open('table_tex.tex', 'w')
outfile.write( "\n".join(outstr))
outfile.close()
