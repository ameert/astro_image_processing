import os
import sys
import numpy as np

indata = np.loadtxt('SerExp_catalog.table', delimiter = ':', usecols = [1])

indata = np.array(indata).T
print indata.shape
print indata
outstr="""\\multicolumn{3}{l}{\\textbf{Trust Total and Component Magnitudes and Sizes}}&  %0.3f &  \\\\ \\hline
& \\multicolumn{2}{l}{\\textbf{Two-Component Galaxies}} &  %0.3f & Figure~\\ref{fig:finalflag_good}, \\ref{fig:some_flag}, \\ref{fig:flip_com}\\\\
& & No Flags &  %0.3f &  Figure~\\ref{fig:finalflag_good} \\\\
& & Good \\Ser{}, Good \\Exp\\ (Some Flags) &  %0.3f &  Figure~\\ref{fig:some_flag} \\\\
& & Flip Components &  %0.3f &  Figure~\\ref{fig:flip_com} \\\\ \\hline
\\multicolumn{3}{l}{\\textbf{Trust Total Magnitudes and Sizes Only}} &  %0.3f &  \\\\ \\hline
& \\multicolumn{2}{l}{\\textbf{Bulge Galaxies}} &  %0.3f & Figure~\\ref{fig:finalflag_flags_bulge:no_exp}, \\ref{fig:finalflag_flags_bulge:ser_dom} \\\\
& &No \\Exp\\ Component, n$_{\\Ser}>$2&  %0.3f & Figure~\\ref{fig:finalflag_flags_bulge:no_exp} \\\\
& &\\Ser{} Dominates Always &  %0.3f & Figure~\\ref{fig:finalflag_flags_bulge:ser_dom} \\\\
& \\multicolumn{2}{l}{\\textbf{Disk Galaxies}} &  %0.3f & Figure~\\ref{fig:finalflag_flags_disk:no_ser}, \\ref{fig:finalflag_flags_disk:no_exp_flip}, \\ref{fig:finalflag_flags_disk:ser_dom_flip}, \\ref{fig:finalflag_flags_disk:exp_dom}, \\ref{fig:finalflag_flags_disk:parallel_com} \\\\
& & No \\Ser{} Component &  %0.3f & Figure~\\ref{fig:finalflag_flags_disk:no_ser} \\\\
& & No \\Exp, n$_{Ser}<$2, Flip Components &  %0.3f & Figure~\\ref{fig:finalflag_flags_disk:no_exp_flip}\\\\
& & \\Ser{} Dominates Always, n$_{\\Ser}<$2 & %0.3f &  Figure~\\ref{fig:finalflag_flags_disk:ser_dom_flip}\\\\
& & \\Exp\\ Dominates Always &  %0.3f & Figure~\\ref{fig:finalflag_flags_disk:exp_dom}\\\\
& & Parallel Components &  %0.3f &  Figure~\\ref{fig:finalflag_flags_disk:parallel_com}\\\\
& \\multicolumn{2}{l}{\\textbf{Problematic Two-Component Galaxies}} & %0.3f & Figure~\\ref{fig:finalflag_flags_2comprob:ser_outer}, \\ref{fig:finalflag_flags_2comprob:exp_inner}, \\ref{fig:finalflag_flags_2comprob:good_ser_bad_exp}, \\ref{fig:finalflag_flags_2comprob:bad_ser_good_exp} \\\\
& & \\Ser{} Outer Only &  %0.3f & Figure~ \\ref{fig:finalflag_flags_2comprob:ser_outer} \\\\
& & \\Exp\\ Inner Only &  %0.3f & Figure~ \\ref{fig:finalflag_flags_2comprob:exp_inner} \\\\
& & Good \\Ser{}, Bad \\Exp, B/T$>=$0.5 &  %0.3f & Figure~\\ref{fig:finalflag_flags_2comprob:good_ser_bad_exp} \\\\
& & Bad \\Ser{}, Good \\Exp, B/T$<$0.5 & %0.3f &  Figure~\\ref{fig:finalflag_flags_2comprob:bad_ser_good_exp} \\\\ 
& & Bulge is point & %0.3f &  Figure~\\ref{fig:finalflag_flags_2comprob:tinybulge} \\\\ \\hline \\hline
\\multicolumn{3}{l}{\\textbf{Bad Total Magnitudes and Sizes}} & %0.3f &  \\\\
\\end{tabular}
"""
outstr = """\\begin{tabular}{l l l c  c  c}
\\multicolumn{3}{l}{\\textbf{Descriptive Category}} &  \\textbf{\\% SerExp} & \\textbf{Example Galaxy} \\\\ \\hline \\hline
"""+outstr %(tuple(indata[:-6]))


outfile = open('serexptable_tex1.tex', 'w')
outfile.write(outstr)
outfile.close()
