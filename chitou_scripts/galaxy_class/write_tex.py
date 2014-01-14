file = open('plots_piece.tex', 'w')

import random as r
from mysql_connect import *

seed = 36
all_numbers = []
times = 20
dba = 'sdss_sample'
usr = 'pymorph'
pwd = 'pymorph'
r.seed(seed)
cursor = mysql_connect(dba,usr,pwd)

all_numbers = []


cmd = 'select galcount from r_full where BT_DevExp < .4 and BT_DevExp > .2 and re_pix_DevExp/rd_pix_DevExp > .5 and fit_DevExp = 1  and fit_Ser = 1 and galcount <3000;'  

cursor.execute(cmd)
rows = cursor.fetchall()
rows = list(rows)
number_list = []
for row in rows:
    number_list.append(row[0])

for count in range(times):
    while 1:
        number = r.choice(number_list)
        print number
        if number not in all_numbers and number not in [2112, 1918, 1949]:
            all_numbers.append(number)
            break

    str = """\\begin{center}
 \centering
 \includegraphics[scale = .65]{/home/ameert/profile_plotting/plots/%06d_fits_1d_DevExp.png}
\end{center}
""" %(number)

    file.write(str+'\n\n')
    for model_type in ['Dev','Ser','DevExp','SerExp']:
        str = """\\begin{center}
 \includegraphics[scale = .65]{/home/ameert/profile_plotting/plots/%06d_fits_comp_%s.png}
\end{center}
""" %(number, model_type)
        file.write(str+'\n\n')



file.close()

        
