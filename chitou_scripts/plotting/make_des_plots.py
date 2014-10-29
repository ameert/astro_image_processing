python cmp_main_des.py -1 des_05 -2 des_05 -m ser -b r -x mtot -y mtot -f -z ser --title "Sextractor auto mag" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "19.5,22.5" --bins "17.0,24.0,0.5" --ylab 'm$_{\mathrm{tot, in}}$-m$_{\mathrm{tot, SEx}}$' --xlab 'm$_{\mathrm{tot, in}}$'
mv r_des_05_des_05_ser_mtot_mtot.eps r_des_05_des_05_ser_mtot_sexmag.eps
python cmp_main_des.py -1 des_05 -2 des_05 -m ser -b r -x mtot -y hrad -f -z ser --title "Sextractor Radius" --yl "-0.5,0.5" --ytM 0.2 --ytm 0.05 --xl "19.5,22.5" --bins "17.0,24.0,0.5"  --xlab 'm$_{\mathrm{tot, in}}$' --ylab '1 - (r$_{\mathrm{SEx}}$/r$_{\mathrm{in}}$)$_{\mathrm{hl}}$'
mv r_des_05_des_05_ser_mtot_hrad.eps r_des_05_des_05_ser_mtot_sexrad.eps



python cmp_main_des.py -1 des_05 -2 des_05 -m ser -b r -x mtot -y mtot -f -z ser --title "PyMorph Ser" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "19.5,22.5" --bins "17.0,24.0,0.5" --ylab 'm$_{\mathrm{tot, in}}$-m$_{\mathrm{tot, pm}}$' --xlab 'm$_{\mathrm{tot, in}}$'
python cmp_main_des.py -1 des_05 -2 des_05 -m ser -b r -x mtot -y hrad -f -z ser --title "PyMorph Ser" --yl "-0.5,0.5" --ytM 0.2 --ytm 0.05 --xl "19.5,22.5" --bins "19.5,24.0,0.5"  --xlab 'm$_{\mathrm{tot, in}}$' --ylab '1 - (r$_{\mathrm{pm}}$/r$_{\mathrm{in}}$)$_{\mathrm{hl}}$'


--ylab 'm$_{\mathrm{tot, in}}$-m$_{\mathrm{tot, pm}}$'

python cmp_main_des.py -1 des_05 -2 des_05 -m ser -b r -x mtot -y mtot -f -z ser --title "PyMorph Ser vs SExtractor" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "19.5,22.5" --bins "17.0,24.0,0.5" --ylab 'm$_{\mathrm{tot, SEx}}$-m$_{\mathrm{tot, pm}}$' --xlab 'm$_{\mathrm{tot, in}}$'
python cmp_main_des.py -1 des_05 -2 des_05 -m ser -b r -x mtot -y hrad -f -z ser --title "PyMorph Ser vs SExtractor" --yl "-0.5,0.5" --ytM 0.2 --ytm 0.05 --xl "19.5,22.5" --bins "19.5,24.0,0.5"  --xlab 'm$_{\mathrm{tot, in}}$' --ylab '1 - (r$_{\mathrm{SEx}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
