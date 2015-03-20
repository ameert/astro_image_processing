python cmp_main.py -1 band -2 band -m serexp -n serexp -b r -d i -x ttype -y BT -f -z serexp  --title "PyMorph r-i"  --yl "-0.2,0.2" --ytM .2 --ytm 0.05  
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d i -x ttype -y BT -f -z serexp  --title "PyMorph g-i"  --yl "-0.2,0.2" --ytM .2 --ytm 0.05  
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d r -x ttype -y BT -f -z serexp  --title "PyMorph g-r"  --yl "-0.2,0.2" --ytM .2 --ytm 0.05  

python cmp_main.py -1 band -2 band -m serexp -n serexp -b r -d i -x ttype -y mtot_abs -f -z serexp  --title "PyMorph r-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab   '(r-i)$_{\mathrm{tot}}$'
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d i -x ttype -y mtot_abs -f -z serexp  --title "PyMorph g-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab   '(g-i)$_{\mathrm{tot}}$'
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d r -x ttype -y mtot_abs -f -z serexp  --title "PyMorph g-r"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-r)$_{\mathrm{tot}}$'

python cmp_main.py -1 cmodel -2 cmodel -m serexp -n serexp -b r -d i -x ttype -y mtot_abs -f -z serexp  --title "CModel r-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab   '(r-i)$_{\mathrm{tot}}$' 
python cmp_main.py -1 cmodel -2 cmodel -m serexp -n serexp -b g -d i -x ttype -y mtot_abs -f -z serexp  --title "CModel g-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-i)$_{\mathrm{tot}}$'
python cmp_main.py -1 cmodel -2 cmodel -m serexp -n serexp -b g -d r -x ttype -y mtot_abs -f -z serexp  --title "CModel g-r"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-r)$_{\mathrm{tot}}$'

python cmp_main.py -1 model -2 model -m serexp -n serexp -b r -d i -x ttype -y mtot_abs -f -z serexp  --title "Model r-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(r-i)$_{\mathrm{tot}}$' 
python cmp_main.py -1 model -2 model -m serexp -n serexp -b g -d i -x ttype -y mtot_abs -f -z serexp  --title "Model g-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab   '(g-i)$_{\mathrm{tot}}$'
python cmp_main.py -1 model -2 model -m serexp -n serexp -b g -d r -x ttype -y mtot_abs -f -z serexp  --title "Model g-r"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-r)$_{\mathrm{tot}}$'
  
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d i -x ttype -y mtot_abs -f -z serexp  --title "PyMorph g-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-i)$_{\mathrm{tot}}$'  
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d r -x ttype -y mtot_abs -f -z serexp  --title "PyMorph g-r"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-r)$_{\mathrm{tot}}$' 
python cmp_main.py -1 band -2 band -m serexp -n serexp -b r -d i -x ttype -y mtot_abs -f -z serexp  --title "PyMorph r-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(r-i)$_{\mathrm{tot}}$'  


python cmp_main.py -1 band -2 band -m ser -n ser -b r -d i -x ttype -y nbulge -f -z ser  --title "PyMorph r-i"  --yl "-1.0,1.0" --ytM .4 --ytm 0.05  
python cmp_main.py -1 band -2 band -m ser -n ser -b g -d i -x ttype -y nbulge -f -z ser  --title "PyMorph g-i"  --yl "-1.0,1.0" --ytM .4 --ytm 0.05  
python cmp_main.py -1 band -2 band -m ser -n ser -b g -d r -x ttype -y nbulge -f -z ser  --title "PyMorph g-r"  --yl "-1.0,1.0" --ytM .4 --ytm 0.05  

python cmp_main.py -1 band -2 band -m serexp -n serexp -b r -d i -x ttype -y nbulge -f -z serexp  --title "PyMorph r-i"  --yl "-1.0,1.0" --ytM .4 --ytm 0.05  
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d i -x ttype -y nbulge -f -z serexp  --title "PyMorph g-i"  --yl "-1.0,1.0" --ytM .4 --ytm 0.05  
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d r -x ttype -y nbulge -f -z serexp  --title "PyMorph g-r"  --yl "-1.0,1.0" --ytM .4 --ytm 0.05  

python cmp_main.py -1 band -2 band -m serexp -n serexp -b r -d i -x ttype -y mdisk_abs -f -z serexp  --title "PyMorph r-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05  --ylab  '(r-i)$_{\mathrm{disk}}$' --conditions "  and f1.galcount = a.galcount and f1.band='r' and f1.model='serexp' and f1.ftype='u' and f2.galcount = a.galcount and f2.band='i' and f2.model='serexp' and f2.ftype='u' and (f1.flag&(pow(2,10)+pow(2,4))>0) and (f2.flag&(pow(2,10)+pow(2,4))>0)" --add_tables ", Flags_catalog as f1, Flags_catalog as f2 " 
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d i -x ttype -y mdisk_abs -f -z serexp  --title "PyMorph g-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05  --ylab '(g-i)$_{\mathrm{disk}}$' --conditions "  and f1.galcount = a.galcount and f1.band='g' and f1.model='serexp' and f1.ftype='u' and f2.galcount = a.galcount and f2.band='i' and f2.model='serexp' and f2.ftype='u' and (f1.flag&(pow(2,10)+pow(2,4))>0) and (f2.flag&(pow(2,10)+pow(2,4))>0)" --add_tables ", Flags_catalog as f1, Flags_catalog as f2 " 
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d r -x ttype -y mdisk_abs -f -z serexp  --title "PyMorph g-r"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05 --ylab  '(g-r)$_{\mathrm{disk}}$' --conditions "  and f1.galcount = a.galcount and f1.band='g' and f1.model='serexp' and f1.ftype='u' and f2.galcount = a.galcount and f2.band='r' and f2.model='serexp' and f2.ftype='u' and (f1.flag&(pow(2,10)+pow(2,4))>0) and (f2.flag&(pow(2,10)+pow(2,4))>0)" --add_tables ", Flags_catalog as f1, Flags_catalog as f2 " 

python cmp_main.py -1 band -2 band -m serexp -n serexp -b r -d i -x ttype -y mbulge_abs -f -z serexp  --title "PyMorph r-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05    --ylab   '(r-i)$_{\mathrm{bulge}}$' --conditions "  and f1.galcount = a.galcount and f1.band='r' and f1.model='serexp' and f1.ftype='u' and f2.galcount = a.galcount and f2.band='i' and f2.model='serexp' and f2.ftype='u' and (f1.flag&(pow(2,10)+pow(2,1))>0) and (f2.flag&(pow(2,10)+pow(2,1))>0)" --add_tables ", Flags_catalog as f1, Flags_catalog as f2 " 
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d i -x ttype -y mbulge_abs -f -z serexp  --title "PyMorph g-i"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05    --ylab    '(g-i)$_{\mathrm{bulge}}$' --conditions "  and f1.galcount = a.galcount and f1.band='g' and f1.model='serexp' and f1.ftype='u' and f2.galcount = a.galcount and f2.band='i' and f2.model='serexp' and f2.ftype='u' and (f1.flag&(pow(2,10)+pow(2,1))>0) and (f2.flag&(pow(2,10)+pow(2,1))>0)" --add_tables ", Flags_catalog as f1, Flags_catalog as f2 " 
python cmp_main.py -1 band -2 band -m serexp -n serexp -b g -d r -x ttype -y mbulge_abs -f -z serexp  --title "PyMorph g-r"  --yl "-0.5,1.5" --ytM .4 --ytm 0.05  --ylab   '(g-r)$_{\mathrm{bulge}}$' --conditions "  and f1.galcount = a.galcount and f1.band='g' and f1.model='serexp' and f1.ftype='u' and f2.galcount = a.galcount and f2.band='r' and f2.model='serexp' and f2.ftype='u' and (f1.flag&(pow(2,10)+pow(2,1))>0) and (f2.flag&(pow(2,10)+pow(2,1))>0)" --add_tables ", Flags_catalog as f1, Flags_catalog as f2 " 
