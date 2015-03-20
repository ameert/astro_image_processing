#r band
python cmp_lackner_simard_agree.py -t simard -m ser -b r -x mtot -y mtot
python cmp_lackner_simard_agree.py -t simard -m ser -b r -x hrad -y hrad
python cmp_lackner_simard_agree.py -t simard -m ser -b r -x mtot -y hrad
python cmp_lackner_simard_agree.py -t simard -m ser -b r -x nbulge -y nbulge
python cmp_lackner_simard_agree.py -t simard -m ser -b r -x mtot -y nbulge

python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mtot -y mtot
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x hrad -y hrad
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mtot -y hrad
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x BT -y BT
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mtot -y BT
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mbulge -y mbulge
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x rbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mdisk -y mdisk
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x rdisk -y rdisk
python cmp_lackner_simard_agree.py -t simard -m devexp -b r -x mdisk -y rdisk

python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mtot -y mtot
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x hrad -y hrad
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mtot -y hrad
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x nbulge -y nbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mtot -y nbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x BT -y BT
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mtot -y BT
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mbulge -y mbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x rbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mdisk -y mdisk
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x rdisk -y rdisk
python cmp_lackner_simard_agree.py -t simard -m serexp -b r -x mdisk -y rdisk

#g band

python cmp_lackner_simard_agree.py -t simard -m ser -b g -x mtot -y mtot
python cmp_lackner_simard_agree.py -t simard -m ser -b g -x hrad -y hrad
python cmp_lackner_simard_agree.py -t simard -m ser -b g -x mtot -y hrad
python cmp_lackner_simard_agree.py -t simard -m ser -b g -x nbulge -y nbulge
python cmp_lackner_simard_agree.py -t simard -m ser -b g -x mtot -y nbulge

python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mtot -y mtot
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x hrad -y hrad
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mtot -y hrad
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x BT -y BT
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mtot -y BT
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mbulge -y mbulge
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x rbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mdisk -y mdisk
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x rdisk -y rdisk
python cmp_lackner_simard_agree.py -t simard -m devexp -b g -x mdisk -y rdisk

python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mtot -y mtot
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x hrad -y hrad
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mtot -y hrad
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x nbulge -y nbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mtot -y nbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x BT -y BT
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mtot -y BT
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mbulge -y mbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x rbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mbulge -y rbulge
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mdisk -y mdisk
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x rdisk -y rdisk
python cmp_lackner_simard_agree.py -t simard -m serexp -b g -x mdisk -y rdisk


mv *simard_lacknermatch*.eps *simard_lacknermatch*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/simard_lackner_match/
