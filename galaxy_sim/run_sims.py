import os
import sys

choice = int(sys.argv[1])
if choice == 1:
    os.system('python make_sims.py 0.03 350000 700000')
elif choice == 2:
    os.system('python make_sims.py 0.03 18563 350000')
elif choice == 3:
    os.system('python make_sims_des.py 0.286 350000 700000')
elif choice == 4:
    os.system('python make_sims_des.py 0.286 0 350000')
