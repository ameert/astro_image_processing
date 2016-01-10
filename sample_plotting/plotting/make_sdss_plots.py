python cmp_main_sdss_sims.py -1 best -2 best -m ser -b r -x mtot -y mtot -f -z ser --title "Sextractor auto mag" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "14.0,17.8" --bins "14.0,18.01,0.5" --ylab 'm$_{\mathrm{tot, in}}$-m$_{\mathrm{tot, SEx}}$' --xlab 'm$_{\mathrm{tot, in}}$'
mv r_best_best_ser_mtot_mtot.eps r_sdss_sdss_ser_mtot_sexmag.eps
python cmp_main_sdss_sims.py -1 best -2 best -m ser -b r -x mtot -y hrad -f -z ser --title "Sextractor Radius" --yl "-0.5,0.5" --ytM 0.2 --ytm 0.05 --xl "14.0,17.8" --bins "14.0,18.01,0.5"  --xlab 'm$_{\mathrm{tot, in}}$' --ylab '1 - (r$_{\mathrm{SEx}}$/r$_{\mathrm{in}}$)$_{\mathrm{hl}}$'
mv r_best_best_ser_mtot_hrad.eps r_sdss_sdss_ser_mtot_sexrad.eps



python cmp_main_sdss_sims.py -1 best -2 best -m ser -b r -x mtot -y mtot -f -z ser --title "PyMorph Ser" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "14.0,17.8" --bins "14.0,18.01,0.5" --ylab 'm$_{\mathrm{tot, in}}$-m$_{\mathrm{tot, pm}}$' --xlab 'm$_{\mathrm{tot, in}}$' --ytl "%0.1f"
mv r_best_best_ser_mtot_mtot.eps r_sdss_sdss_ser_mtot_mtot.eps
python cmp_main_sdss_sims.py -1 best -2 best -m ser -b r -x mtot -y hrad -f -z ser --title "PyMorph Ser" --yl "-0.5,0.5" --ytM 0.2 --ytm 0.05 --xl "14.0,17.8" --bins "14.0,18.01,0.5"  --xlab 'm$_{\mathrm{tot, in}}$' --ylab '1 - (r$_{\mathrm{pm}}$/r$_{\mathrm{in}}$)$_{\mathrm{hl}}$'
mv r_best_best_ser_mtot_hrad.eps r_sdss_sdss_ser_mtot_hrad.eps



python cmp_main_sdss_sims.py -1 psf -2 sn05 -m ser -b r -x mtot -y mtot -f -z ser --title "" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "14.0,17.8" --bins "14.0,18.01,0.5" --ylab 'm$_{\mathrm{tot, in}}$-m$_{\mathrm{tot, pm}}$' --xlab 'm$_{\mathrm{tot, in}}$' --ytl "%0.1f"
