import os
import sys

choice = int(sys.argv[1])
if choice == 1:
    os.system('python make_sims.py ser 0 112000')
    os.system('python make_sims.py  devexp 0 112000')
    os.system('python make_sims.py  serexp 0 112000')
elif choice == 2:
    os.system('python make_sims.py  ser 112000 216000')
    os.system('python make_sims.py  devexp 112000 216000')
    os.system('python make_sims.py  serexp 112000 216000')
elif choice == 3:
    os.system('python make_sims.py  ser  216000 316000')
    os.system('python make_sims.py  devexp  216000 316000')
    os.system('python make_sims.py  serexp  216000 316000')
elif choice == 4:
    os.system('python make_sims.py  ser  316000 430000')
    os.system('python make_sims.py  devexp  316000 430000')
    os.system('python make_sims.py  serexp  316000 430000')
elif choice == 5:
    os.system('python make_sims.py  ser  430000 534000')
    os.system('python make_sims.py  devexp  430000 534000')
    os.system('python make_sims.py  serexp  430000 534000')
elif choice == 6:
    os.system('python make_sims.py  ser 534000 700000')
    os.system('python make_sims.py  devexp 534000 700000')
    os.system('python make_sims.py  serexp 534000 700000')
