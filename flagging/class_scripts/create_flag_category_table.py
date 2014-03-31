import os
import sys
import numpy as np

fulltab=True

if fulltab:
    models = ['Dev','Ser', 'DevExp','SerExp']
else:
    models = ['Test','SerExp', 'DevExp']

row1str = ' c '*len(models)
row2str = ["""\\textbf{{\% {modname}}}""".format(modname=modname) for modname in models]

row2str = ' & '.join(row2str)

indata = []

for mod in models:
    indat1 = np.loadtxt('%s_catalog.table' %mod, delimiter = ':', usecols = [1])
    indata.append(indat1)

indata = np.array(indata).T
print indata.shape


outstr="""\\multicolumn{3}{l}{\\textbf{Trust Total and Component Magnitudes and Sizes}}&  %s  \\\\ \\hline
& \\multicolumn{2}{l}{\\textbf{Two-Component Galaxies}} &  %s \\\\
& & No Flags &  %s \\\\
& & Good \\Ser{}, Good \\Exp\\ (Some Flags) &  %s  \\\\
& & Flip Components &  %s \\\\ \\hline
\\multicolumn{3}{l}{\\textbf{Trust Total Magnitudes and Sizes Only}} &  %s \\\\ \\hline
& \\multicolumn{2}{l}{\\textbf{Bulge Galaxies}} &  %s \\\\
& &No \\Exp\\ Component, n$_{\\Ser}>$2&  %s \\\\
& &\\Ser{} Dominates Always &  %s \\\\
& \\multicolumn{2}{l}{\\textbf{Disk Galaxies}} &  %s \\\\
& & No \\Ser{} Component &  %s \\\\
& & No \\Exp, n$_{Ser}<$2, Flip Components &  %s \\\\
& & \\Ser{} Dominates Always, n$_{\\Ser}<$2 & %s \\\\
& & \\Exp\\ Dominates Always &  %s \\\\
& & Parallel Components &  %s \\\\
& \\multicolumn{2}{l}{\\textbf{Problematic Two-Component Galaxies}} & %s \\\\
& & \\Ser{} Outer Only &  %s \\\\
& & \\Exp\\ Inner Only &  %s \\\\
& & Good \\Ser{}, Bad \\Exp, B/T$>=$0.5 &  %s \\\\
& & Bad \\Ser{}, Good \\Exp, B/T$<$0.5 & %s \\\\ 
& & Bulge is point & %s \\\\ \\hline \\hline
\\multicolumn{3}{l}{\\textbf{Bad Total Magnitudes and Sizes}} & %s \\\\
& \multicolumn{2}{l}{Centering Problems} & %s \\\\
& \multicolumn{2}{l}{\Ser{} Component Contamination by Neighbors or Sky} & %s \\\\
& \multicolumn{2}{l}{\Exp\ Component Contamination by Neighbors or Sky} & %s \\\\ 
& \multicolumn{2}{l}{Bad \Ser{} and Bad \Exp\ Components} & %s \\\\
& \multicolumn{2}{l}{\galfit{} Failure} & %s \\\\
& \multicolumn{2}{l}{Polluted or Fractured} & %s \\\\
\\end{tabular}
"""

intup = []
for rowcount, row in enumerate(indata):
    print rowcount, row
    rowvals = ['%0.3f' %a for a in row]
    rowvals = ' & '.join(rowvals)
    intup.append(rowvals)

if fulltab:
    outstr = """\\begin{tabular}{l l l c c  c  c}
\\multicolumn{3}{l}{\\textbf{Descriptive Category}} &  \\textbf{\\% Dev}&  \\textbf{\\% Ser} & \\textbf{\\% DevExp} & \\textbf{\\% SerExp} \\\\ \\hline \\hline
"""+outstr %(tuple(intup))
else:
    outstr = """\\begin{tabular}{l l l c  c  c}
\\multicolumn{3}{l}{\\textbf{Descriptive Category}} &  \\textbf{\\% Test} & \\textbf{\\% SerExp} & \\textbf{\\% DevExp} \\\\ \\hline \\hline
"""+outstr %(tuple(intup))

if fulltab:
    outfile = open('full_table_tex.tex', 'w')
else:
    outfile = open('table_tex.tex', 'w')
outfile.write(outstr)
outfile.close()
