#sdss plots rband dev plots
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag -y mtot -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag -y mtot -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model ='dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)"  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag -y hrad -f -z dev --title "PyMorph vs SDSS, (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag -y hrad -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag_abs -y mtot -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag_abs -y mtot -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model ='dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)"  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23,-17" --bins "-22.5,-17.49,0.5"

python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag_abs -y hrad -f -z dev --title "PyMorph vs SDSS, ffracdev>=0.8" --conditions " and c.fracdev_r >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag_abs -y hrad -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-22.5,-17.49,0.5" --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 sdss -m dev -b r -x petrorad -y hrad -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05
python cmp_main.py -1 band -2 sdss -m dev -b r -x petrorad -y hrad -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05


python cmp_main.py -1 band -2 sdss -m dev -b r -x sky -y mtot -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 sdss -m dev -b r -x sky -y  mtot_abs -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag -y sky  -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 "
python cmp_main.py -1 band -2 sdss -m dev -b r -x petromag_abs -y sky  -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 " --xl "-24.0,-19" --bins "-24.0,-18.99,0.5"
python cmp_main.py -1 band -2 sdss -m dev -b r -x petrorad -y sky  -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_r >=0.8 "

#mv r_band_sdss_*.eps r_band_sdss_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/


# lackner dev comparisons
python cmp_main.py -1 band -2 lackner -m dev -b r -x petromag -y mtot -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -2 sdss -1 lackner -m dev -b r -x petromag -y mtot --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -1 band -2 lackner -m dev -b r -x petromag_abs -y mtot -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23,-17" --bins "-22.5,-17.49,0.5" 

python cmp_main.py -2 sdss -1 lackner -m dev -b r -x petromag_abs -y mtot --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"  --xl "-23,-17" --bins "-22.5,-17.49,0.5"


python cmp_main.py -1 band -2 lackner -m dev -b r -x petromag -y hrad -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'




python cmp_main.py -2 sdss -1 lackner -m dev -b r -x petromag -y hrad --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05  --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{LG12}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 lackner -m dev -b r -x petromag_abs -y hrad -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'

python cmp_main.py -2 sdss -1 lackner -m dev -b r -x petromag_abs -y hrad --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{LG12}}$)$_{\mathrm{hl}}$'


#mv r_band_lackner_*.eps r_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/
#mv r_lackner_sdss_*.eps r_lackner_sdss_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/

# ser comparison

python cmp_main.py -1 band -2 simard -m ser -b r -x petromag -y mtot -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag -y rbulge -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag -y nbulge -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x petrorad -y nbulge -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25

python cmp_main.py -1 band -2 simard -m ser -b r -x petromag_abs -y mtot -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag_abs -y rbulge -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag_abs -y nbulge -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m ser -b r -x petrorad_abs -y nbulge -f -z ser --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25


python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x petromag -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x petromag_abs -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --xl "-22,-17" --xtM 1 --xtm 0.25 --yl "-1,1" --ytM 1 --ytm 0.25 --ytl "%d"

python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x petromag -f -z ser --add_tables ", r_simard_fit as sfit " --conditions " and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   "  --title "PyMorph vs S11 "
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x petromag_abs -f -z ser --add_tables ", r_simard_fit as sfit " --conditions " and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " --title "PyMorph vs S11" --xl "-25,-17" --xtM 1 --xtm 0.25 --yl "-1,1" --ytM 1 --ytm 0.25 --ytl "%d"





python cmp_main.py -1 band -2 sdss -m ser -n dev -b r -y sky -x petromag -f -z ser --add_tables ", r_simard_fit as sfit " --conditions " and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   "  --title "PyMorph vs SDSS "
python cmp_main.py -1 band -2 sdss -m ser -n dev -b r -y sky -x petromag_abs -f -z ser --add_tables ", r_simard_fit as sfit " --conditions " and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " --title "PyMorph vs SDSS" --xl "-25,-17" --xtM 1 --xtm 0.25 --yl "-1,1" --ytM 1 --ytm 0.25 --ytl "%d"

python cmp_main.py -1 simard -2 sdss -m ser -n dev -b r -y sky -x petromag -f -z ser --add_tables ", r_simard_fit as sfit " --conditions " and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   "  --title "Simard vs SDSS "
python cmp_main.py -1 simard -2 sdss -m ser -n dev -b r -y sky -x petromag_abs -f -z ser --add_tables ", r_simard_fit as sfit " --conditions " and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " --title "Simard vs SDSS" --xl "-25,-17" --xtM 1 --xtm 0.25 --yl "-1,1" --ytM 1 --ytm 0.25 --ytl "%d"



python cmp_main.py -1 band -2 simard -m ser -b r -x petromag -y mtot -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag -y rbulge -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x petrorad -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-1,1" --ytM 0.5 --ytm 0.25

python cmp_main.py -1 band -2 simard -m ser -b r -x petromag_abs -y mtot -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" --title "PyMorph vs S11 (LG12 sample)" -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag_abs -y rbulge -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" --title "PyMorph vs S11 (LG12 sample)"  -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m ser -b r -x petromag_abs -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" --title "PyMorph vs S11 (LG12 sample)" -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m ser -b r -x petrorad -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " --conditions " and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32   " -p "_lackner_only" --title "PyMorph vs S11 (LG12 sample)" -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"

#mv r_band_simard_*.eps r_band_simard_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/simard/


python cmp_main.py -1 band -2 lackner -m ser -b r -x petromag -y mtot -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b r -x petromag -y rbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025  --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m ser -b r -x petromag -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 lackner -m ser -b r -x petrorad -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25

python cmp_main.py -1 band -2 lackner -m ser -b r -x petromag_abs -y mtot -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 band -2 lackner -m ser -b r -x petromag_abs -y rbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"  --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m ser -b r -x petromag_abs -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 band -2 lackner -m ser -b r -x petrorad -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25

python cmp_main.py -1 simard -2 lackner -m ser -b r -x petromag -y mtot -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 simard -2 lackner -m ser -b r -x petromag -y rbulge -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 simard -2 lackner -m ser -b r -x petromag -y nbulge -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 simard -2 lackner -m ser -b r -x petrorad -y nbulge -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25

python cmp_main.py -1 simard -2 lackner -m ser -b r -x petromag_abs -y mtot -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 simard -2 lackner -m ser -b r -x petromag_abs -y rbulge -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 simard -2 lackner -m ser -b r -x petromag_abs -y nbulge -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 simard -2 lackner -m ser -b r -x petrorad -y nbulge -f -z ser  --title "Simard vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", r_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25

#mv r_band_lackner_*.eps r_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/
#mv r_simard_lackner_*.eps r_simard_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/


# DevExp comparisons


python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y mtot -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x petrorad -y hrad -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025 --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y hrad -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y BT -f -z devexp --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit "  -u 100
python cmp_main.py -1 band -2 simard -m devexp -b r -x BT -y BT -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y mbulge -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y rbulge -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y mdisk -f -z devexp --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y rdisk -f -z devexp --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'









python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y mtot -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petrorad -y hrad -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y hrad -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y BT -f -z devexp --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit "  -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x BT -y BT -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y mbulge -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y rbulge -f -z devexp  --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y mdisk -f -z devexp --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y rdisk -f -z devexp --title "PyMorph vs S11 (S11 sample)" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'




python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y mtot -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4' " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y hrad -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025 --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x BT -y BT -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y BT -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y mbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y rbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y mdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag -y rdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'






python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y mtot -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4' " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01  --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y hrad -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x BT -y BT -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y BT -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y mbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y rbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y mdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 simard -m devexp -b r -x petromag_abs -y rdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11 (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'


#mv r_band_simard_*.eps r_band_simard_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/simard/


python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y mtot -f -z devexp --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petrorad -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b r -x BT -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y mbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y rbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y mdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag -y rdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'



python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y mtot -f -z devexp --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petrorad -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b r -x BT -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y mbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y rbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y mdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b r -x petromag_abs -y rdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'





python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y mtot -f -z devexp --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petrorad -y hrad -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y hrad -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x BT -y BT -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y BT -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y mbulge -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y rbulge -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y mdisk -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag -y rdisk -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{disk}}$'





python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y mtot -f -z devexp --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01  --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petrorad -y hrad -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y hrad -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"  --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x BT -y BT -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y BT -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y mbulge -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y rbulge -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y mdisk -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 simard -2 lackner -m devexp -b r -x petromag_abs -y rdisk -f -z devexp  --title "Simard vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{S11}}$)$_{\mathrm{disk}}$'


#mv r_band_lackner_*.eps r_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/
#mv r_simard_lackner_*.eps r_simard_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/


# Serexp fits

python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y mtot -f -z serexp   --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m serexp -b r -x petrorad -y hrad -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025    --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y hrad -f -z serexp   --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y nbulge -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100   --yl "-2,2" --ytM 1 --ytm 0.25
python cmp_main.py -1 band -2 simard -m serexp -b r -x BT -y BT -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y BT -f -z serexp   --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y mbulge -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y rbulge -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100  --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y mdisk -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag -y rdisk -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'







python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y mtot -f -z serexp   --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m serexp -b r -x petrorad -y hrad -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y hrad -f -z serexp   --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y nbulge -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"    --yl "-2,2" --ytM 1 --ytm 0.25
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y BT -f -z serexp   --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" 
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y mbulge -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" 
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y rbulge -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y mdisk -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" 
python cmp_main.py -1 band -2 simard -m serexp -b r -x petromag_abs -y rdisk -f -z serexp  --title "PyMorph vs S11 (S11 sample)"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"   --ylab '1 - (r$_{\mathrm{S11}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$' 

#mv r_band_simard_*.eps r_band_simard_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/simard/

# sdss best comparisons

python cmp_main.py -1 band -2 sdss -m best -n petro -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 sdss -m best -n petro -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5"
python cmp_main.py -1 band -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample" 
python cmp_main.py -1 band -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5"


python cmp_main.py -1 band -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "PyMorph vs SDSS (Men14 sample)" --conditions "  and lfit.galcount = a.galcount and x.flag&pow(2,19)=0 " --add_tables ", r_mendel_best as lfit " -p "_mendel_only" 
python cmp_main.py -1 band -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot    --title "PyMorph vs SDSS (Men14 sample)" --conditions "  and lfit.galcount = a.galcount  and x.flag&pow(2,19)=0 " --add_tables ", r_mendel_best as lfit " -p "_mendel_only" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5" 
python cmp_main.py -1 simard -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "S11 vs SDSS (Men14 sample)" --conditions "  and lfit.galcount = a.galcount  and x.flag&pow(2,19)=0 " --add_tables ", r_mendel_best as lfit " -p "_mendel_only"
python cmp_main.py -1 simard -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot    --title "S11 vs SDSS (Men14 sample)" --conditions "  and lfit.galcount = a.galcount  and x.flag&pow(2,19)=0 " --add_tables ", r_mendel_best as lfit " -p "_mendel_only" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5" 

python cmp_main.py -1 mendel -2 sdss -m best -n petro -b r -x petromag -y mtot  --title "Men14 vs SDSS (Men14 sample)" -p "_mendel_only"  --conditions "  and x.flag&pow(2,19)=0 "
python cmp_main.py -1 mendel -2 sdss -m best -n petro -b r -x petromag_abs -y mtot  --title "Men14 vs SDSS (Men14 sample)" -p "_mendel_only" --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --conditions "  and x.flag&pow(2,19)=0 "
python cmp_main.py -1 mendel -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot  --title "Men14 vs SDSS (Men14 sample)" -p "_mendel_only" --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"  --conditions "  and  x.flag&pow(2,19)=0 "
python cmp_main.py -1 mendel -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "Men14 vs SDSS (Men14 sample)" -p "_mendel_only" --conditions "  and x.flag&pow(2,19)=0 "




python cmp_main.py -1 simard -2 sdss -m best -n petro -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 simard -2 sdss -m best -n petro -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 simard -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 simard -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"


python cmp_main.py -1 lackner -2 sdss -m best -n petro -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 sdss -m best -n petro -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"

python cmp_main.py -1 band -2 simard -m best -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 simard -m best -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 mendel -m best -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 mendel -m best -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"

python cmp_main.py -1 lackner -2 band -m best -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 band -m best -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 simard -m best -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 simard -m best -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 mendel -m best -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 mendel -m best -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"


python cmp_main.py -1 mendel -2 sdss -m best -n petro -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample" --conditions "  and lfit.galcount = a.galcount " --add_tables ", r_lackner_fit as lfit " -p "_lackner_only" 
python cmp_main.py -1 mendel -2 sdss -m best -n petro -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample" --conditions "  and lfit.galcount = a.galcount " --add_tables ", r_lackner_fit as lfit " -p "_lackner_only" 
python cmp_main.py -1 mendel -2 sdss -m best -n cmodel -b r -x petromag -y mtot  --title "PyMorph vs SDSS, full sample" --conditions "  and lfit.galcount = a.galcount " --add_tables ", r_lackner_fit as lfit " -p "_lackner_only" 
python cmp_main.py -1 mendel -2 sdss -m best -n cmodel -b r -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample" --conditions "  and lfit.galcount = a.galcount " --add_tables ", r_lackner_fit as lfit " -p "_lackner_only" 

#mv r_band_model_*.eps r_band_model_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/
#mv r_*_cmodel_*.eps r_*_cmodel_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/cmodel/
#mv r_band_petro_*.eps r_band_petro_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/
mv r_band_sdss_*.eps r_sdss_cmodel_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/cmodel/
mv r_simard_sdss_cmodel*.eps r_simard_sdss_cmodel_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/cmodel/
mv r_mendel_sdss_cmodel*.eps r_mendel_sdss_cmodel_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/cmodel/
mv r_lackner_sdss_cmodel*.eps r_lackner_sdss_cmodel_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/cmodel/

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x BT -y nbulge -f -z serexp  --title "PyMorph Serexp-Ser"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-3,3"

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x BT -y mtot -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-.1,0.2" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" 

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x BT -y hrad -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-.3,0.3" --ytM 0.1 --ytm 0.025 --ytl "%0.2f" --ylab '1 - (r$_{\mathrm{Ser}}$/r$_{\mathrm{Ser-Exp}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x petromag_abs -y mtot -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-.1,0.2" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x petromag_abs -y hrad -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-.3,0.3" --ytM 0.1 --ytm 0.025 --ytl "%0.2f"  --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{Ser}}$/r$_{\mathrm{Ser-Exp}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x petromag -y mtot -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-.1,0.2" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"  --bins "14.0,18.01,0.5"

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x petromag -y hrad -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "-.3,0.3" --ytM 0.1 --ytm 0.025 --ytl "%0.2f" --bins "14.0,18.01,0.5" --ylab '1 - (r$_{\mathrm{Ser}}$/r$_{\mathrm{Ser-Exp}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x BT -y nbulge -f -z serexp  --title "PyMorph Serexp-Ser"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and 
y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y "
 --yl "-3,3"

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x BT -y rbulge -f -z serexp  --title "PyMorph Serexp-Ser"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and 
y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y " --yl "0.0,1.2" --ytM .2 --ytm 0.05  --ylab 'r$_{\mathrm{Ser-Exp, bulge}}$/r$_{\mathrm{Ser, hl}}$'

#mv r_band_band_*.eps r_band_band_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/best_model/

#and a.r_bulge*sqrt(a.ba_bulge)>0.5*c.PSFWidth_r 

python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b r -x BT -y BT -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95 " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b r -x BT -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-4,2" --ytM 1 --ytm 0.1
python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b r -x BT -y BT -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.4" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b r -x BT -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,4" --ytM 1 --ytm 0.1


python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b r -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-4,2" --ytM 1 --ytm 0.1  --xl "0,4" --xtM 1 --xtm 0.1

python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b r -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,4" --ytM 1 --ytm 0.1  --xl "0,4" --xtM 1 --xtm 0.1


#mv r_band_lackner_nb*[.eps,.tbl] /home/ameert/git_projects/catalog2013/figures/cmp_plots/best_model/
