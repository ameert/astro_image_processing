#sdss plots rband dev plots
python cmp_main.py -1 band -2 sdss -m dev -b r -x mtot -y mtot -f -z dev --title "PyMorph vs SDSS, fracdev=1" --conditions " and c.fracdev_r =1 " --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"
python cmp_main.py -1 band -2 sdss -m dev -b r -x mtot -y mtot -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model ='dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS, L12 sample"  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -1 band -2 sdss -m dev -b r -x mtot -y hrad -f -z dev --title "PyMorph vs SDSS, ffracdev=1" --conditions " and c.fracdev_r =1 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05
python cmp_main.py -1 band -2 sdss -m dev -b r -x mtot -y hrad -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05

python cmp_main.py -1 band -2 sdss -m dev -b r -x hrad -y hrad -f -z dev --title "PyMorph vs SDSS, fracdev=1" --conditions " and c.fracdev_r =1 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05
python cmp_main.py -1 band -2 sdss -m dev -b r -x hrad -y hrad -f -z dev --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS, L12 sample"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05


python cmp_main.py -1 band -2 sdss -m dev -b r -x sky -y mtot -f -z dev --title "PyMorph vs SDSS, full sample" --conditions " and c.fracdev_r =1 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 sdss -m dev -b r -x sky -y  mtot_abs -f -z dev --title "PyMorph vs SDSS, full sample" --conditions " and c.fracdev_r =1 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 sdss -m dev -b r -x sky -y hrad -f -z dev --title "PyMorph vs SDSS, full sample" --conditions " and c.fracdev_r =1 "
python cmp_main.py -1 band -2 sdss -m dev -b r -x mtot -y sky  -f -z dev --title "PyMorph vs SDSS, full sample" --conditions " and c.fracdev_r =1 "
python cmp_main.py -1 band -2 sdss -m dev -b r -x mtot_abs -y sky  -f -z dev --title "PyMorph vs SDSS, full sample" --conditions " and c.fracdev_r =1 "
python cmp_main.py -1 band -2 sdss -m dev -b r -x hrad -y sky  -f -z dev --title "PyMorph vs SDSS, full sample" --conditions " and c.fracdev_r =1 "

#mv r_band_sdss_*.eps r_band_sdss_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/


# lackner dev comparisons
python cmp_main.py -1 band -2 lackner -m dev -b r -x mtot -y mtot -f -z dev --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -1 band -2 lackner -m dev -b r -x mtot -y hrad -f -z dev --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05

python cmp_main.py -1 band -2 lackner -m dev -b r -x hrad -y hrad -f -z dev --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", r_lackner_fit as lfit " -u 50  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05

#mv r_band_lackner_*.eps r_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/

# ser comparisons

python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y mtot -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x hrad -y hrad -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y hrad -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x rbulge -y rbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y rbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x nbulge -y nbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25 
python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y nbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x hrad -y nbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x rbulge -y nbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y mtot -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 --xl "-1.0,0.5" --xtM 0.5 --xtm 0.25 --xtl "%0.1f"
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y mtot_abs -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 --xl "-1.0,0.5" --xtM 0.5 --xtm 0.25 --xtl "%0.1f"
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y hrad -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit "
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y rbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit "
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x mtot -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit "
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x mtot_abs -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit " --xl "-23,-16" --xtM 1 --xtm 0.25 --yl "-0.75,0.5" --ytM 0.25 --ytm 0.05 --ytl "%0.2f"
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x hrad -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit "
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x rbulge -f -z ser --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 > 0.32 " --add_tables ", r_simard_fit as sfit "

python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y mtot -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x hrad -y hrad -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y hrad -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x rbulge -y rbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y rbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m ser -b r -x nbulge -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x mtot -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x hrad -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x rbulge -y nbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"  --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y mtot -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y mtot_abs -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 --xl "-1.0,0.5" --xtM 0.5 --xtm 0.25 --xtl "%0.1f"
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y hrad -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m ser -b r -x sky -y rbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x mtot -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x mtot_abs -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --xl "-22,-17" --xtM 1 --xtm 0.25 --yl "-0.75,0.5" --ytM 0.25 --ytm 0.05 --ytl "%0.2f"
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x hrad -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m ser -b r -y sky -x rbulge -f -z ser --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'ser'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"

#mv r_band_simard_*.eps r_band_simard_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/simard/


python cmp_main.py -1 band -2 lackner -m ser -b r -x mtot -y mtot -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b r -x hrad -y hrad -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b r -x mtot -y hrad -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b r -x rbulge -y rbulge -f -z ser   --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b r -x mtot -y rbulge -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b r -x nbulge -y nbulge -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 lackner -m ser -b r -x mtot -y nbulge -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 lackner -m ser -b r -x hrad -y nbulge -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 lackner -m ser -b r -x rbulge -y nbulge -f -z ser  --title "PyMorph vs L12, L12 sample" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'ser' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25

#mv r_band_lackner_*.eps r_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/


# DevExp comparisons


python cmp_main.py -1 band -2 simard -m devexp -b r -x mtot -y mtot -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x hrad -y hrad -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m devexp -b r -x mtot -y hrad -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m devexp -b r -x BT -y BT -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 
python cmp_main.py -1 band -2 simard -m devexp -b r -x mtot -y BT -f -z devexp --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit "  -u 100
python cmp_main.py -1 band -2 simard -m devexp -b r -x mbulge -y mbulge -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m devexp -b r -x rbulge -y rbulge -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m devexp -b r -x mbulge -y rbulge -f -z devexp  --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m devexp -b r -x mdisk -y mdisk -f -z devexp --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x rdisk -y rdisk -f -z devexp --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x mdisk -y rdisk -f -z devexp --title "PyMorph vs S11, S11 sample" --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS > 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01

python cmp_main.py -1 band -2 simard -m devexp -b r -x mtot -y mtot -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4' " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x hrad -y hrad -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m devexp -b r -x mtot -y hrad -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m devexp -b r -x BT -y BT -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m devexp -b r -x mtot -y BT -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m devexp -b r -x mbulge -y mbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m devexp -b r -x rbulge -y rbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m devexp -b r -x mbulge -y rbulge -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample"
python cmp_main.py -1 band -2 simard -m devexp -b r -x mdisk -y mdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x rdisk -y rdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 simard -m devexp -b r -x mdisk -y rdisk -f -z devexp --add_tables ", r_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'nb4'  " -p "_lackner_only" -u 100 --title "PyMorph vs S11, L12 sample" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01

#mv r_band_simard_*.eps r_band_simard_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/simard/


python cmp_main.py -1 band -2 lackner -m devexp -b r -x mtot -y mtot -f -z devexp --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b r -x hrad -y hrad -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m devexp -b r -x mtot -y hrad -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m devexp -b r -x BT -y BT -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x mtot -y BT -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x mbulge -y mbulge -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x rbulge -y rbulge -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x mbulge -y rbulge -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b r -x mdisk -y mdisk -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b r -x rdisk -y rdisk -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b r -x mdisk -y rdisk -f -z devexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01

#mv r_band_lackner_*.eps r_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/


# Serexp fits

python cmp_main.py -1 band -2 simard -m serexp -b r -x mtot -y mtot -f -z serexp   --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m serexp -b r -x hrad -y hrad -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 simard -m serexp -b r -x mtot -y hrad -f -z serexp   --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 simard -m serexp -b r -x nbulge -y nbulge -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100   --yl "-2,2" --ytM 1 --ytm 0.25
python cmp_main.py -1 band -2 simard -m serexp -b r -x mbulge -y nbulge -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-2,2" --ytM 1 --ytm 0.25
python cmp_main.py -1 band -2 simard -m serexp -b r -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100 --yl "-2,2" --ytM 1 --ytm 0.25
python cmp_main.py -1 band -2 simard -m serexp -b r -x BT -y BT -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x mtot -y BT -f -z serexp   --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x mbulge -y mbulge -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x rbulge -y rbulge -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x mbulge -y rbulge -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x mdisk -y mdisk -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x rdisk -y rdisk -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100
python cmp_main.py -1 band -2 simard -m serexp -b r -x mdisk -y rdisk -f -z serexp  --title "PyMorph vs S11, S11 sample"  --conditions "  and sfit.galcount = a.galcount and sfit.Prob_n4 <= 0.32 and sfit.Prob_pS <= 0.32 " --add_tables ", r_simard_fit as sfit " -u 100

#mv r_band_simard_*.eps r_band_simard_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/simard/

# sdss best comparisons

python cmp_main.py -1 band -2 petro -m serexp -b r -x mtot -y mtot -f -z serexp  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 petro -m serexp -b r -x mtot -y hrad -f -z serexp  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 petro -m serexp -b r -x hrad -y hrad -f -z serexp  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 model -m serexp -b r -x mtot -y mtot -f -z serexp --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 cmodel -m serexp -b r -x mtot -y mtot -f -z serexp  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 cmodel -m serexp -b r -x mtot_abs -y BT -f -z serexp  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 cmodel -m serexp -b r -x mtot_abs -y mtot_abs -f -z serexp  --title "PyMorph vs SDSS, full sample"
#mv r_band_model_*.eps r_band_model_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/
#mv r_band_petro_*.eps r_band_petro_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/
#mv r_band_cmodel_*.eps r_band_cmodel_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/

python cmp_main.py -1 band -2 band -m serexp -n ser -b r -x BT -y nbulge -f -z serexp  --title "PyMorph Ser/Serexp, L12"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'r' and y.ftype = 'u' and 
y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_optimize as y "

#mv r_band_band_*.eps r_band_band_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/best_model/

#and a.r_bulge*sqrt(a.ba_bulge)>0.5*c.PSFWidth_r 

python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b r -x BT -y BT -f -z serexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95 " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b r -x BT -y nbulge -f -z serexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-4,2" --ytM 1 --ytm 0.1
python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b r -x BT -y BT -f -z serexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-0.2,0.4" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b r -x BT -y nbulge -f -z serexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,4" --ytM 1 --ytm 0.1


python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b r -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-4,2" --ytM 1 --ytm 0.1  --xl "0,4" --xtM 1 --xtm 0.1

python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b r -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs L12, L12 sample"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", r_lackner_fit as lfit " -u 100 --yl "-1,4" --ytM 1 --ytm 0.1  --xl "0,4" --xtM 1 --xtm 0.1


#mv r_band_lackner_nb*[.eps,.tbl] /home/ameert/git_projects/catalog2013/figures/cmp_plots/best_model/
