fit_flags = [('Bad Central Fit', 0), 
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
             #("Bad TOTAL fit", 12),
             #("Bad disk fit", 13),
             #("Bad bulge fit", 14),
             ]

class_flags = [('Contamination from nearby source',0 ),
               ('Background Problems', 1), 
               ('Crowded field',2), 
               ('Evidence of past or present interaction',3),
               ('Asymmetry',4),
               ('Low Surface Brightness',5),
               ('Bar Component Evident',6)]

finalflag_vals = [('TOTAL FIT', 0),
                  ('m_tot', 1),
                  ('r_tot',2),
                  ('BT', 3),
                  ('m_bulge', 4),
                  ('r_bulge', 5),
                  ('n_bulge', 6),
                  ('ba_bulge', 7),
                  ('pa_bulge', 8),
                  ('m_disk', 9),
                  ('r_disk', 10),
                  ('ba_disk', 11),
                  ('pa_disk', 12),
                  ('neighbor fit', 13)
                  ]

new_finalflag_vals = [
                      ('centering', 0),
                      ('parallel components', 1),
                      ('no bulge likely', 2),     #4     
                      ('no disk likely', 3),
       
                      ('bulge contaminated', 4), #16
                      ('bulge is sky', 5),
                      ('high e bulge', 6),          
                      ('bulge pa problem', 7),
                      ('bulge fitting outer', 8),   
                      ('bulge is disk', 9),         
                      ('bulge dominates always', 10), #1024                  
                      ('low n bulge', 11), #2048

                      ('disk contaminated', 12), #4096
                      ('disk is sky', 13),
                      ('high e disk', 14),
                      ('disk pa problem', 15),      
                      ('disk fitting inner', 16),   
                      ('disk dominates always', 17),
                                                          
                      ('galfit failure', 18),      #262144
                      ('Bad total fit', 19),       #524288
                      ('bad disk', 20),
                      ('bad bulge', 21),
                      ('high chi^2', 22),
                      ('flip components', 23),


                      ]


new_finalflag_dict = dict(new_finalflag_vals)
 

#these are stored as flag 'u' in the flags_optimize table
category_flag = [("Good Total Magnitudes and Sizes", 0),

                 ("\tBulge Galaxies", 1),
                 ("\t\tNo Exp Component, n$_{Ser}>=$2", 2),
                 ( "\t\tSer Dominates Always, n$_{Ser}>=$2", 3),

                 ("\tDisk Galaxies", 4),
                 ("\t\tNo Ser Component", 5),
                 ( "\t\tNo Exp, n$_{Ser}<$2, Flip Components", 6),
                 ( "\t\tSer Dominates Always, n$_{Ser}<$2", 7),
                 ("\t\tExp Dominates Always", 8),
                 ( "\t\tParallel Components", 9),
                 
                 ("\tTwo-Component Galaxies", 10),       #64
                 ("\t\tNo Flags", 11),   #128
                 ("\t\tGood Ser, Good Exp (Some Flags)", 12),          #256
                 ("\t\tFlip Components, n$_{Ser}<$2", 13),         #512
                 
                 ("\tProblem Two-Component Galaxies", 14),
                 ("\t\tSer Outer Only", 15),
                 ("\t\tExp Inner Only", 16),
                 ("\t\tGood Ser, Bad Exp, B/T$>=$0.5", 17),
                 ("\t\tBad Ser, Good Exp, B/T$<$0.5", 18),

                 ("Bad Total Magnitudes and Sizes", 19),
                 ("\tCentering Problems", 20),      #8388608
                 ("\tSer Component Contamination", 21), 
                 ("\tExp Component Contamination", 22),
                 ("\tBad Ser and Bad Exp Components", 23),      #8388608
                 ("\tGalfit Failure", 24),      #8388608
                 ]


category_flag_dict = dict(category_flag)

def check_flags(flag, flagbit):
    if flag>=0:
        if flagbit == -1:
            is_good = (flag == 0)
        else:
            is_good = (flag & 2**flagbit)==2**flagbit

    else: 
        is_good = False
    return is_good
 
