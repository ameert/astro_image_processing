#r band
python cmp_main.py -1 band -2 nsatlas -m ser -b r -x petromag -f -z ser -y mtot --title "PyMorph vs NASA-Sloan" --yl "-0.15,0.15" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"
python cmp_main.py -1 band -2 nsatlas -m ser -b r -x petromag_abs -f -z ser -y mtot --title "PyMorph vs NASA-Sloan" --yl "-0.15,0.15" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23.0,-17" --bins "-22.5.0,-16.99,0.5"
python cmp_main.py -1 simard -2 nsatlas -m ser -b r -x petromag -f -z ser -y mtot --title "S11 vs NASA-Sloan" --yl "-0.15,0.15" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"
python cmp_main.py -1 simard -2 nsatlas -m ser -b r -x petromag_abs -f -z ser -y mtot --title "S11 vs NASA-Sloan" --yl "-0.15,0.15" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23.0,-17" --bins "-22.5.0,-16.99,0.5"





python cmp_main.py -1 band -2 nsatlas -m ser -b r -x petromag -f -z ser -y nbulge --title "PyMorph vs NASA-Sloan" --yl "-1,1" --ytM 0.5 --ytm 0.25 --ytl "%0.2f"
python cmp_main.py -1 band -2 nsatlas -m ser -b r -x petromag_abs -f -z ser -y nbulge --title "PyMorph vs NASA-Sloan" --yl "-1,1" --ytM 0.5 --ytm 0.25 --ytl "%0.2f" --xl "-23.0,-17" --bins "-22.5.0,-16.99,0.5"
python cmp_main.py -1 simard -2 nsatlas -m ser -b r -x petromag -f -z ser -y nbulge --title "S11 vs NASA-Sloan" --yl "-1,1" --ytM 0.5 --ytm 0.25 --ytl "%0.2f"
python cmp_main.py -1 simard -2 nsatlas -m ser -b r -x petromag_abs -f -z ser -y nbulge --title "S11 vs NASA-Sloan" --yl "-1,1" --ytM 0.5 --ytm 0.25 --ytl "%0.2f" --xl "-23.0,-17" --bins "-22.5.0,-16.99,0.5"


python cmp_main.py -1 band -2 nsatlas -m serexp -n ser -b r -x petromag -f -z serexp -y mtot --title "PyMorph vs NASA-Sloan" --yl "-0.15,0.15" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"  -p "_ourserexp"
python cmp_main.py -1 band -2 nsatlas -m serexp -n ser -b r -x petromag_abs -f -z serexp -y mtot --title "PyMorph vs NASA-Sloan" --yl "-0.15,0.15" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23.0,-17" --bins "-22.5.0,-16.99,0.5" -p "_ourserexp"





#mv *nsatlas*.eps *nsatlas*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/simard/
