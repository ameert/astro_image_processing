import os
import sys
import numpy as np

fulltab=False

if fulltab:
    models = ['Dev','Ser', 'DevExp','SerExp']
else:
    models = ['Dev','Ser','DevExp','SerExp','Test']

row1str = ' c '*len(models)
row2str = ["""\\textbf{{\% {modname}}}""".format(modname=modname) for modname in models]

row2str = ' & '.join(row2str)

indata = []

for mod in models:
    indat1 = np.loadtxt('%s_catalog.table' %mod, delimiter = ':', usecols = [1])
    indata.append(indat1)

indata = np.array(indata).T
print indata.shape


outstr="""-- & \\multicolumn{3}{l}{\\textbf{Trust Total and Component Magnitudes and Sizes}}&  %s  \\\\ \\hline
10 & & \\multicolumn{2}{l}{\\textbf{Two-Component Galaxies}} &  %s \\\\
11 & & & No Flags &  %s \\\\
12 & & & Good \\Ser{}, Good \\Exp\\ (Some Flags) &  %s  \\\\
13 & & & Flip Components &  %s \\\\ \\hline
-- & \\multicolumn{3}{l}{\\textbf{Trust Total Magnitudes and Sizes Only}} &  %s \\\\ \\hline
1 & & \\multicolumn{2}{l}{\\textbf{Bulge Galaxies}} &  %s \\\\
2 & & &No \\Exp\\ Component, n$_{\\Ser}>$2&  %s \\\\
3 & & &\\Ser{} Dominates Always &  %s \\\\
4 & & \\multicolumn{2}{l}{\\textbf{Disk Galaxies}} &  %s \\\\
5 & & & No \\Ser{} Component &  %s \\\\
6 & & & No \\Exp, n$_{Ser}<$2, Flip Components &  %s \\\\
7 & & & \\Ser{} Dominates Always, n$_{\\Ser}<$2 & %s \\\\
8 & & & \\Exp\\ Dominates Always &  %s \\\\
9 & & & Parallel Components &  %s \\\\
14 & & \\multicolumn{2}{l}{\\textbf{Problematic Two-Component Galaxies}} & %s \\\\
15 & & & \\Ser{} Outer Only &  %s \\\\
16 & & & \\Exp\\ Inner Only &  %s \\\\
17 & & & Good \\Ser{}, Bad \\Exp, B/T$>=$0.5 &  %s \\\\
18 & & & Bad \\Ser{}, Good \\Exp, B/T$<$0.5 & %s \\\\ 
26 & & & Bulge is point & %s \\\\ \\hline \\hline
19 & \\multicolumn{3}{l}{\\textbf{Bad Total Magnitudes and Sizes}} & %s \\\\
20 & & \multicolumn{2}{l}{Centering Problems} & %s \\\\
21 & & \multicolumn{2}{l}{\Ser{} Component Contamination by Neighbors or Sky} & %s \\\\
22 & & \multicolumn{2}{l}{\Exp\ Component Contamination by Neighbors or Sky} & %s \\\\ 
23 & & \multicolumn{2}{l}{Bad \Ser{} and Bad \Exp\ Components} & %s \\\\
24 & & \multicolumn{2}{l}{\galfit{} Failure} & %s \\\\
25 & & \multicolumn{2}{l}{Polluted or Fractured} & %s \\\\
\\end{tabular}
"""

intup = []
for rowcount, row in enumerate(indata):
    print rowcount, row
    rowvals = ['%0.3f' %a for a in row]
    rowvals = ' & '.join(rowvals)
    intup.append(rowvals)

if fulltab:
    outstr = """\\begin{tabular}{l l l l c c  c  c}
\\multicolumn{3}{l}{\\textbf{Descriptive Category}} &   \\textbf{\\% DevExp} & \\textbf{\\% SerExp} \\\\ \\hline \\hline
"""+outstr %(tuple(intup))
else:
    outstr = """\\begin{tabular}{l l l l c  c  c c c}
\\textbf{Flag Bit} & \\multicolumn{3}{l}{\\textbf{Descriptive Category}} &  \\textbf{\\% Dev}&  \\textbf{\\% Ser}& \\textbf{\\% DevExp}  & \\textbf{\\% SerExp} &\\textbf{\\% Test} \\\\ \\hline \\hline
"""+outstr %(tuple(intup))

if fulltab:
    outfile = open('full_table_tex.tex', 'w')
else:
    outfile = open('table_tex.tex', 'w')
outfile.write(outstr)
outfile.close()
