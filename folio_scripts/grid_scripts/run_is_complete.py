from is_complete import *

choice = 2

if choice == 1:
    for model in ['ser', 'devexp','serexp','dev']:
        for count in range(1,80):
            incat = '/data2/home/ameert/stripe82/data/dr7/r/sdss_r_%d.cat' %count
            outcat = '/data2/home/ameert/stripe82/fits/dr7_r_%s/%d/result.csv' %(model,count)

            if not check_done(incat, outcat, doneness = 0.05):
                print "%s%d" %(model, count)

elif choice == 2:
    for model,ms in zip(['ser', 'devexp','serexp'], ['s','de','se']):
        for ms2 in ['s','de','se']:
            for count in range(1,11):
                incat = '/data2/home/ameert/final_sim/data/20/%s_chip_%d.cat' %(model,count)
                outcat = '/data2/home/ameert/final_sim/fits/cutout_size/%s/cutn%s20%s/%d/result.csv' %(model,ms,ms2,count)

                if not check_done(incat, outcat, doneness = 0.05):
                    print "cutn%s20%s %d" %(ms,ms2, count)
elif choice == 3:
    for model,ms in zip(['ser', 'devexp','serexp'], ['s','de','se']):
        for ms2 in ['s','de','se']:
            for count in range(1,11):
                incat = '/data2/home/ameert/final_sim/data/20/%s_flat_%d.cat' %(model,count)
                outcat = '/data2/home/ameert/final_sim/fits/flat/%s/flat%s20%s/%d/result.csv' %(model,ms,ms2,count)
                
                if not check_done(incat, outcat, doneness = 0.05):
                    print "flat%s20%s %d" %(ms,ms2, count)
                    

elif choice == 4:
    for model,ms in zip(['ser', 'devexp','serexp'], ['s','de','se']):
        for ms2 in ['s','de','se']:
            for count in range(1,11):
                incat = '/data2/home/ameert/final_sim/data/25/%s_chip_%d.cat' %(model,count)
                outcat = '/data2/home/ameert/final_sim/fits/cutout_size/%s/cutn%s25%s/%d/result.csv' %(model,ms,ms2,count)

                a = check_done(incat, outcat, doneness = 0.05)
                if not a[0]:
                    print "cutn%s25%s %d" %(ms,ms2, count)
                    print a[1], a[2]


