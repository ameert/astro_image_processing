autoflag_vals = [
                  ('centering', 0),
                  ('parallel components', 1),
                  ('no bulge likely', 2),          
                  ('no disk likely', 3),
                  
                  ('bulge contaminated', 4), 
                  ('bulge is sky', 5),
                  ('high e bulge', 6),          
                  ('bulge pa problem', 7),
                  ('bulge fitting outer', 8),   
                  ('bulge is disk', 9),         
                  ('bulge dominates always', 10),                   
                  ('low n bulge', 11), 
                  
                  ('disk contaminated', 12), 
                  ('disk is sky', 13),
                  ('high e disk', 14),
                  ('disk pa problem', 15),      
                  ('disk fitting inner', 16),   
                  ('disk dominates always', 17),
                  
                  ('galfit failure', 18),      
                  ('Bad total fit', 19),       
                  ('bad disk', 20),
                  ('bad bulge', 21),
                  ('high chi^2', 22),
                  ('flip components', 23),
                  ]

autoflag_dict = dict(autoflag_vals)

#these are stored as flag 'u' in the flags_optimize table
uflag_vals = [("Good Total Magnitudes and Sizes", 0),
              
              ("\tBulge Galaxies", 1),
              ("\t\tNo Exp Component, n$_{Ser}>=$2", 2),
              ( "\t\tSer Dominates Always, n$_{Ser}>=$2", 3),
              
              ("\tDisk Galaxies", 4),
              ("\t\tNo Ser Component", 5),
              ( "\t\tNo Exp, n$_{Ser}<$2, Flip Components", 6),
              ( "\t\tSer Dominates Always, n$_{Ser}<$2", 7),
              ("\t\tExp Dominates Always", 8),
              ( "\t\tParallel Components", 9),
                 
              ("\tTwo-Component Galaxies", 10),      
              ("\t\tNo Flags", 11),   
              ("\t\tGood Ser, Good Exp (Some Flags)", 12),          
              ("\t\tFlip Components, n$_{Ser}<$2", 13),        
              
              ("\tProblemmatic Two-Component Galaxies", 14),
              ("\t\tSer Outer Only", 15),
              ("\t\tExp Inner Only", 16),
              ("\t\tGood Ser, Bad Exp, B/T$>=$0.5", 17),
              ("\t\tBad Ser, Good Exp, B/T$<$0.5", 18),

              ("Bad Total Magnitudes and Sizes", 19),
              ("\tCentering Problems", 20),     
              ("\tSer Component Contamination by Neighbors or Sky", 21), 
              ("\tExp Component Contamination by Neighbors or Sky", 22),
              ("\tBad Ser and Bad Exp Components", 23),      
              ("\tGalfit Failure", 24),    
              ]

uflag_dict = dict(uflag_vals)

visualflag_vals =  [('Bad Central Fit', 0), 
                    ("Bad Middle Fit",1), 
                    ("Bad Outer Fit",2),
                    (r'\Ser\ Fitting Outer Part of the Galaxy',3), 
                    (r'\Exp\ Fitting Inner Part of the Galaxy', 4), 
                    ('Centering Problems', 5), 
                    ('Sky Subtraction Problems', 6), 
                    (r'\Ser/\Exp\ Position Angle Difference', 7), 
                    (r'High Ellipticity \Exp Component', 8),
                    (r'High Ellipticity \Ser Component', 9), 
                    (r"Large \Exp Radius/\Exp Fitting Sky", 10),
                    ("Bad Fit of Sub-Dominant Second Component", 11),
                    ]
visualflag_dict = dict(visualflag_vals)

visclass_vals = [
                 ('Contamination from nearby source',0 ),
                 ('Background Problems', 1), 
                 ('Crowded field',2), 
                 ('Evidence of past or present interaction',3),
                 ('Asymmetry',4),
                 ('Low Surface Brightness',5),
                 ('Bar Component Evident',6),
                 ]
visclass_dict = dict(visclass_vals)

autoflag_config = {
                   'max_sep':0.7, #70% of SEx Hrad
                   'chicut': 20.0,
                   'posang_d':{'ba_cut':0.75,
                               'pa_cut':45.0
                               },
                   
                   'bulge_cut':lambda BT,mag: 1000.0*(0.2-BT)**3+mag-19.0>0.5,
                   #no_bulge = np.where(data['BT']<0.05,1,0) | np.where(data['r_bulge']*np.sqrt(data['ba_bulge'])<0.396/2, 1,0)
                   'disk_cut' :lambda BT,mag: 1000.0*(BT-0.8)**3+mag-19.0>0.5,
                   'par_com':0.1,
                   'disky_n':2.0,

                   'disk_rad_cut':2.7,
                   'disk_sky_cut':3.0,
                   'disk_sky_ba':0.6,
                   'disk_ba_cut':0.4,
                   'disk_ba_BT':0.75,
                   'disk_dom_light':0.95,
                   
                   'bulge_light_cut':0.9,
                   'bulge_sky_cut':4.0,
                   'bulge_sky_ba':0.6,
                   'bulge_ba_cut':0.4,
                   'bulge_ba_BT':0.25,
                   'bulge_disk_rat':1.5,
                   'bulge_dom_light':0.95,
                   }
