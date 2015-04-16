from mysql_class import *
import numpy as np

filter = 'r'

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

tot_gals, = cursor.get_data('select count(*) from CAST;')
tot_gals = len(tot_gals)

for model in ['dev']:#, 'ser','devexp','serexp']:
    # collect the data
    cmd = 'select Ie, Id, re_pix, re_kpc, rd_pix, rd_kpc, n, eb, ed, bpa, dpa, BT, chi2nu, num_targets, flag, fitflag from full_dr7_r_%s order by galcount;'

    data = cursor.get_data(cmd)

    data_dict = {}
    for dat, key in zip(data, ['Ie', 'Id', 're_pix', 're_kpc', 'rd_pix', 'rd_kpc', 'n', 'eb', 'ed', 'bpa', 'dpa', 'BT','chi2nu', 'num_targets', 'flag', 'fitflag']):
        data_dict[key] = np.array(data)


    # Now open the report file
    outfile = open('report_%s.tex' %model)

    outfile.write("""\begin{table}
       \begin{tabular}{l|l|l|l}
       \textbf{condition}& \textbf{indicator used} & \textbf{Number of galaxies} & \textbf{Percent of galaxies} \\ \hline
       """)

    
    












    outfile.write("""   \end{tabular}
       \caption{Table of various flag conditions and other possible problem cases for the %s fit of the %s band SDSS data}
       \end{table}
       """ %(model, filter))
    
       
