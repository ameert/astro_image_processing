# sdss plots
python cmp_sdss_new.py -t petro -m serexp -b r -x mtot -y mtot -f 
python cmp_sdss_new.py -t petro -m serexp -b r -x hrad -y hrad -f
python cmp_sdss_new.py -t petro -m serexp -b r -x mtot -y hrad -f
python cmp_sdss_new.py -t model -m serexp -b r -x mtot -y mtot -f
python cmp_sdss_new.py -t dev -m dev -b r -x mtot -y mtot -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x mtot -y hrad -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x hrad -y hrad -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x batot -y batot -f -z dev 
python cmp_sdss_new.py -t dev -m dev -b r -x mtot -y batot -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x sky -y mtot -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x sky -y hrad -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x mtot -y sky -f -z dev
python cmp_sdss_new.py -t dev -m dev -b r -x hrad -y sky -f -z dev


python cmp_sdss_new.py -t petro -m best -b g -x mtot -y mtot
python cmp_sdss_new.py -t petro -m best -b g -x hrad -y hrad
python cmp_sdss_new.py -t petro -m best -b g -x mtot -y hrad
python cmp_sdss_new.py -t model -m best -b g -x mtot -y mtot
python cmp_sdss_new.py -t dev -m dev -b g -x mtot -y mtot
python cmp_sdss_new.py -t dev -m dev -b g -x mtot -y hrad
python cmp_sdss_new.py -t dev -m dev -b g -x hrad -y hrad
python cmp_sdss_new.py -t dev -m dev -b g -x batot -y batot
python cmp_sdss_new.py -t dev -m dev -b g -x mtot -y batot
python cmp_sdss_new.py -t dev -m dev -b g -x sky -y mtot
python cmp_sdss_new.py -t dev -m dev -b g -x sky -y hrad

python cmp_sdss_new.py -t petro -m best -b i -x mtot -y mtot
python cmp_sdss_new.py -t petro -m best -b i -x hrad -y hrad
python cmp_sdss_new.py -t petro -m best -b i -x mtot -y hrad
python cmp_sdss_new.py -t model -m best -b i -x mtot -y mtot
python cmp_sdss_new.py -t dev -m dev -b i -x mtot -y mtot
python cmp_sdss_new.py -t dev -m dev -b i -x mtot -y hrad
python cmp_sdss_new.py -t dev -m dev -b i -x hrad -y hrad
python cmp_sdss_new.py -t dev -m dev -b i -x batot -y batot
python cmp_sdss_new.py -t dev -m dev -b i -x mtot -y batot
python cmp_sdss_new.py -t dev -m dev -b i -x sky -y mtot
python cmp_sdss_new.py -t dev -m dev -b i -x sky -y hrad


mv *_dev_dev_*.eps *_dev_dev_*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/sdss/

mv *_model_best_*.eps *_model_best_*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/sdss/

mv *_petro_best_*.eps *_petro_best_*.tbl /home/ameert/svn_stuff/catalog_paper/papers/data/trunk/figures/cmp_plots/sdss/
