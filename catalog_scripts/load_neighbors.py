#!/data2/home/ameert/python/bin/python2.5

#create table ser_neighborvals (galcount int, neighbornum int, xctr float, yctr float, n_ser float, r_ser float, ba_ser float, pa_ser float);
#Alter table ser_neighborvals add unique key (galcount, neighbornum);

import numpy as np
from mysql_class import *
import sys
import os

def get_neighbornum(file):
    if os.path.isfile(file):
        infile = open(file)
        inlines = infile.readlines()
        infile.close()
        
        for count, a in enumerate(inlines):
            a = a.split('#')[0]
            inlines[count]=a

        for count, a in enumerate(inlines):
            if 'sky' in a:
                if '0)' in a:
                    break
        inlines= inlines[count:]
                
        for count, a in enumerate(inlines):
            if 'sersic' in a:
                if '0)' in a:
                    break
        inlines= inlines[count:]
                

        inlines= '\n'.join(inlines)
        neighborcount = "".join(inlines)
    else:
        neighborcount = ""
    return neighborcount

def get_vals(nn):
    neighbors = nn.split(' 0)')[1:]
    nnum=[]
    xc=[]
    yc=[]
    m_ser=[]
    n_ser=[]
    r_ser=[]
    ba_ser=[]
    pa_ser=[]
    for a in neighbors:
        nnum.append(len(nnum)+1)
        a= a.split(' 1) ')[1]
        a= a.split(' 3) ')
        pos = a[0]
        ol = len(pos)
        nl = -1
        while ol != nl:
            ol=nl
            pos = pos.replace('  ',' ')
            nl = len(pos)
        pos = pos.split(' ')
        
        print pos
        xc.append(float(pos[0]))
        yc.append(float(pos[1]))

        a= a[1].split(' 4) ')
        pos = a[0].split(' ')
        m_ser.append(float(pos[0]))

        a= a[1].split(' 5) ')
        pos = a[0].split(' ')
        r_ser.append(float(pos[0]))

        a= a[1].split(' 6) ')
        pos = a[0].split(' ')
        n_ser.append(float(pos[0]))

        a= a[1].split(' 8) ')
        a= a[1].split(' 9) ')
        pos = a[0].split(' ')
        ba_ser.append(float(pos[0]))

        a= a[1].split('10) ')
        pos = a[0].split(' ')
        pa_ser.append(float(pos[0]))
    
    return nnum, xc, yc, m_ser, n_ser, r_ser, ba_ser, pa_ser

model = sys.argv[1]
band = sys.argv[2]
folder = int(sys.argv[3])

folder_path = '/data2/home/ameert/catalog/%s/fits/%s/%04d/' %(band,model,folder)

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
host = 'shredder'

conn = mysql_connect(dba, usr, pwd, host)

os.system('ls '+folder_path+'/G_*stamp.out > file%d.list' %folder)

infile = open('file%d.list' %folder)
for line in infile:
    line = line.strip()
    galcount = line.split('/')[-1]
    galcount = int(galcount.split('_')[2])
    name = line.split('G_')[1]
    name = name.split('.out')[0]
    nn = get_neighbornum(line)
    nnum, xc, yc, m_ser, n_ser, r_ser, ba_ser, pa_ser= get_vals(nn)
    for a in zip(nnum, xc, yc, m_ser, n_ser, r_ser, ba_ser, pa_ser):
        cmd = 'insert ignore into %s_neighborvals values (%d, %d, %f,%f,%f,%f,%f,%f,%f);' %(model, galcount,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7])
        print cmd
        conn.execute(cmd)
    
infile.close()

os.system('rm file%d.list' %folder)

