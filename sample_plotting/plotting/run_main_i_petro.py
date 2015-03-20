#sdss plots gband dev plots
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag -y mtot -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag -y mtot -f -z dev --add_tables ", i_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model ='dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)"  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag -y hrad -f -z dev --title "PyMorph vs SDSS, (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag -y hrad -f -z dev --add_tables ", i_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag_abs -y mtot -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag_abs -y mtot -f -z dev --add_tables ", i_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model ='dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)"  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23,-17" --bins "-22.5,-17.49,0.5"

python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag_abs -y hrad -f -z dev --title "PyMorph vs SDSS, ffracdev>=0.8" --conditions " and c.fracdev_g >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag_abs -y hrad -f -z dev --add_tables ", i_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)" --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-22.5,-17.49,0.5" --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'

#python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petrorad -y hrad -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05
#python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petrorad -y hrad -f -z dev --add_tables ", i_lackner_fit as lfit " --conditions " and lfit.galcount = a.galcount and lfit.model = 'dvc' " -p "_lackner_only" -u 50 --title "PyMorph vs SDSS (LG12 sample)"  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05


python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x sky -y mtot -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x sky -y  mtot_abs -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag -y sky  -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 "
python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petromag_abs -y sky  -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 " --xl "-24.0,-19" --bins "-24.0,-18.99,0.5"
#python cmp_main.py -1 band -2 sdss -m dev -b i -d i -x petrorad -y sky  -f -z dev --title "PyMorph vs SDSS (fracdev>=0.8)" --conditions " and c.fracdev_g >=0.8 "

#mv i_band_sdss_*.eps i_band_sdss_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/sdss/
mv i_band_i_sdss_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/

# lackner dev comparisons
python cmp_main.py -1 band -2 lackner -m dev -b i -d i -x petromag -y mtot -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -2 sdss -1 lackner -m dev -b i -d i -x petromag -y mtot --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"

python cmp_main.py -1 band -2 lackner -m dev -b i -d i -x petromag_abs -y mtot -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-23,-17" --bins "-22.5,-17.49,0.5" 

python cmp_main.py -2 sdss -1 lackner -m dev -b i -d i -x petromag_abs -y mtot --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50  --yl "-0.15,0.1" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"  --xl "-23,-17" --bins "-22.5,-17.49,0.5"


python cmp_main.py -1 band -2 lackner -m dev -b i -d i -x petromag -y hrad -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'




python cmp_main.py -2 sdss -1 lackner -m dev -b i -d i -x petromag -y hrad --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05  --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{LG12}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 lackner -m dev -b i -d i -x petromag_abs -y hrad -f -z dev --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'

python cmp_main.py -2 sdss -1 lackner -m dev -b i -d i -x petromag_abs -y hrad --title "LG12 vs SDSS (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and lfit.model = 'dvc' " --add_tables ", i_lackner_fit as lfit " -u 50 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{SDSS}}$/r$_{\mathrm{LG12}}$)$_{\mathrm{hl}}$'


#mv i_band_lackner_*.eps i_band_lackner_*.tbl ~/git_projects/catalog2013/figures/cmp_plots/lackner/
#mv i_lackner_sdss_*.eps i_lackner_sdss_*.tbl ~/git_projects/catalog2013/figures/cmp_plots/sdss/

mv i_band_i_lackner_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/lackner/
mv i_lackner_i_sdss_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/
mv i_band_i_sdss_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/

# ser comparison

python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petromag -y mtot -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petromag -y rbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025  --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petromag -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25
python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petrorad -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25

python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petromag_abs -y mtot -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petromag_abs -y rbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"  --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petromag_abs -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.05 --xl "-23,-17" --bins "-23.0,-16.99,0.5"
python cmp_main.py -1 band -2 lackner -m ser -b i -d i -x petrorad -y nbulge -f -z ser  --title "PyMorph vs LG12 (LG12 sample)" --conditions "  and lfit.galcount = a.galcount and sfit.galcount = a.galcount and sfit.Prob_Ps > 0.32  " --add_tables ", i_lackner_fit as lfit, r_simard_fit as sfit " -u 100 --yl "-1,1" --ytM 0.5 --ytm 0.25


#mv i_band_lackner_*.eps i_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/
#mv i_band_i_lackner_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/lackner/

# DevExp comparisons

python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y mtot -f -z devexp --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petrorad -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x BT -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y mbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y rbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y mdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag -y rdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'



python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y mtot -f -z devexp --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100  --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petrorad -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"   --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y hrad -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.3,0.3" --ytM 0.1 --ytm 0.025  --xl "-23,-17" --bins "-22.5,-17.49,0.5"    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{hl}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x BT -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y BT -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y mbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y rbulge -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --xl "-23,-17" --bins "-22.5,-17.49,0.5"    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{bulge}}$'
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y mdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"
python cmp_main.py -1 band -2 lackner -m devexp -b i -d i -x petromag_abs -y rdisk -f -z devexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.01 --xl "-23,-17" --bins "-22.5,-17.49,0.5"    --ylab '1 - (r$_{\mathrm{LG12}}$/r$_{\mathrm{pm}}$)$_{\mathrm{disk}}$'


#mv i_band_lackner_*.eps i_band_lackner_*.tbl /home/ameert/git_projects/catalog2013/figures/cmp_plots/lackner/

mv i_band_i_lackner_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/lackner/
mv i_lackner_g_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/lackner/
mv i_band_i_sdss_* ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/


# sdss best comparisons

python cmp_main.py -1 band -2 sdss -m best -n petro -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 band -2 sdss -m best -n petro -b i -d i -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5"
python cmp_main.py -1 band -2 sdss -m best -n cmodel -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS, full sample" 
python cmp_main.py -1 band -2 sdss -m best -n cmodel -b i -d i -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5"


python cmp_main.py -1 band -2 sdss -m best -n cmodel -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS (Joint sample)" --conditions "  and lfit.galcount = a.galcount and x.flag&pow(2,20)=0 " --add_tables ", r_mendel_best as lfit " -p "_joint_only" 
python cmp_main.py -1 band -2 sdss -m best -n cmodel -b i -d i -x petromag_abs -y mtot    --title "PyMorph vs SDSS (Joint sample)" --conditions "  and lfit.galcount = a.galcount  and x.flag&pow(2,20)=0 " --add_tables ", r_mendel_best as lfit " -p "_joint_only" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5" 

python cmp_main.py -1 band -2 sdss -m best -n petro -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS (Joint sample)" --conditions "  and lfit.galcount = a.galcount and x.flag&pow(2,20)=0 " --add_tables ", r_mendel_best as lfit " -p "_joint_only" 
python cmp_main.py -1 band -2 sdss -m best -n petro -b i -d i -x petromag_abs -y mtot    --title "PyMorph vs SDSS (Joint sample)" --conditions "  and lfit.galcount = a.galcount  and x.flag&pow(2,20)=0 " --add_tables ", r_mendel_best as lfit " -p "_joint_only" --xl "-24.0,-16" --bins "-24.0,-15.99,0.5" 

python cmp_main.py -1 lackner -2 sdss -m best -n petro -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 sdss -m best -n petro -b i -d i -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 sdss -m best -n cmodel -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 sdss -m best -n cmodel -b i -d i -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 band -m best -b i -d i -x petromag -y mtot  --title "PyMorph vs SDSS, full sample"
python cmp_main.py -1 lackner -2 band -m best -b i -d i -x petromag_abs -y mtot  --title "PyMorph vs SDSS, full sample"


mv i_band_i_model_*.eps i_band_i_model_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/
mv i_*_i_cmodel_*.eps i_*_i_cmodel_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/cmodel/
mv i_band_i_sdss_petro_*.eps i_band_i_sdss_petro_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/

mv i_band_i_sdss_cmodel*.eps i_band_i_sdss_cmodel_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/cmodel/
mv i_lackner_i_sdss_cmodel*.eps i_lackner_i_sdss_cmodel_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/cmodel/
mv i_lackner_i_band_best_*.eps i_lackner_i_band_best_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/best_model/
mv i_lackner_i_sdss_cmodel*.eps i_lackner_i_sdss_cmodel_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/cmodel/
mv i_lackner_i_sdss_petro_*.eps i_lackner_i_sdss_petro_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/sdss/

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x BT -y nbulge -f -z serexp  --title "PyMorph Serexp-Ser"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-3,3"

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x BT -y mtot -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-.1,0.2" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" 

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x BT -y hrad -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-.3,0.3" --ytM 0.1 --ytm 0.025 --ytl "%0.2f" --ylab '1 - (r$_{\mathrm{Ser}}$/r$_{\mathrm{Ser-Exp}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x petromag_abs -y mtot -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-.1,0.199999" --ytM 0.05 --ytm 0.025 --ytl "%0.2f" --xl "-24.0,-17" --bins "-24.0,-16.99,0.5"

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x petromag_abs -y hrad -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-.299999999,0.29999999" --ytM 0.1 --ytm 0.025 --ytl "%0.2f"  --xl "-24.0,-17" --bins "-24.0,-16.99,0.5" --ylab '1 - (r$_{\mathrm{Ser}}$/r$_{\mathrm{Ser-Exp}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x petromag -y mtot -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-.1,0.2" --ytM 0.05 --ytm 0.025 --ytl "%0.2f"  --bins "14.0,18.01,0.5"

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x petromag -y hrad -f -z serexp  --title "PyMorph Serexp-Ser "  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,4)>0 or x.flag&pow(2,1)>0 or x.flag&pow(2,10)>0 or x.flag&pow(2,14)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-.3,0.3" --ytM 0.1 --ytm 0.025 --ytl "%0.2f" --bins "14.0,18.01,0.5" --ylab '1 - (r$_{\mathrm{Ser}}$/r$_{\mathrm{Ser-Exp}}$)$_{\mathrm{hl}}$'

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x BT -y nbulge -f -z serexp  --title "PyMorph Serexp-Ser"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and 
y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y "
 --yl "-3,3"

python cmp_main.py -1 band -2 band -m serexp -n ser -b i -d i -x BT -y rbulge -f -z serexp  --title "PyMorph Serexp-Ser"  --conditions "  and a.n_bulge < 7.95 and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.galcount = y.galcount  and y.band = 'i' and y.ftype = 'u' and 
y.model = 'ser' and ( y.flag&pow(2,0)>0) " --add_tables ",Flags_catalog as y " --yl "-1.0,0.2" --ytM .2 --ytm 0.05  --ylab '1-(r$_{\mathrm{Ser-Exp, bulge}}$/r$_{\mathrm{Ser, hl}}$)'

#mv i_band_i_band_*.eps i_band_i_band_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/best_model/
mv i_band_i_band_*.eps i_band_i_band_*.tbl ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/best_model/

#and a.r_bulge*sqrt(a.ba_bulge)>0.5*c.PSFWidth_g 

python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b i -d i -x BT -y BT -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95 " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.2,0.2" --ytM 0.1 --ytm 0.025 
python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b i -d i -x BT -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-4,2" --ytM 1 --ytm 0.1
python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b i -d i -x BT -y BT -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-0.2,0.4" --ytM 0.1 --ytm 0.025
python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b i -d i -x BT -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-1,4" --ytM 1 --ytm 0.1


python cmp_main.py -1 band -2 lackner -m serexp -n nb4 -b i -d i -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-4,2" --ytM 1 --ytm 0.1  --xl "0,4" --xtM 1 --xtm 0.1

python cmp_main.py -1 band -2 lackner -m serexp -n nb1 -b i -d i -x rbulge -y nbulge -f -z serexp  --title "PyMorph vs LG12 (LG12 sample)"  --conditions "  and lfit.galcount = a.galcount and lfit.model = 'nb1'  and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0 or x.flag&pow(2,1)>0) and a.n_bulge < 7.95  " --add_tables ", i_lackner_fit as lfit " -u 100 --yl "-1,4" --ytM 1 --ytm 0.1  --xl "0,4" --xtM 1 --xtm 0.1


#mv i_band_i_lackner_nb*[.eps,.tbl] ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/best_model/
mv i_band_i_lackner_nb*[.eps,.tbl] ~/git_projects/thesis/catalog_analysis/figures/EPS/cmp_plots/best_model/

