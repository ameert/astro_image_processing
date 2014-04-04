#r band
python cmp_external.py -t nsatlas -m ser -b r -x mtot -y mtot
python cmp_external.py -t nsatlas -m ser -b r -x mtot_abs -y mtot_abs
python cmp_external.py -t nsatlas -m ser -b r -x n -y n
python cmp_external.py -t nsatlas -m ser -b r -x mtot -y n
python cmp_external.py -t nsatlas -m ser -b r -x mtot_abs -y n


#mv *nsatlas*.eps *nsatlas*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/simard/
