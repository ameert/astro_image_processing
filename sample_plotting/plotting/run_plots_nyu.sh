python cmp_external.py -t nyu -m ser -b r -x mtot -y mtot
python cmp_external.py -t nyu -m ser -b r -x hrad -y hrad
python cmp_external.py -t nyu -m ser -b r -x mtot -y hrad
python cmp_external.py -t nyu -m ser -b r -x nbulge -y nbulge
python cmp_external.py -t nyu -m ser -b r -x mtot -y nbulge

python cmp_external.py -t nyu -m ser -b g -x mtot -y mtot
python cmp_external.py -t nyu -m ser -b g -x hrad -y hrad
python cmp_external.py -t nyu -m ser -b g -x mtot -y hrad
python cmp_external.py -t nyu -m ser -b g -x nbulge -y nbulge
python cmp_external.py -t nyu -m ser -b g -x mtot -y nbulge

python cmp_external.py -t nyu -m ser -b i -x mtot -y mtot
python cmp_external.py -t nyu -m ser -b i -x hrad -y hrad
python cmp_external.py -t nyu -m ser -b i -x mtot -y hrad
python cmp_external.py -t nyu -m ser -b i -x nbulge -y nbulge
python cmp_external.py -t nyu -m ser -b i -x mtot -y nbulge

mv *nyu*.eps *nyu*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/nyu/
