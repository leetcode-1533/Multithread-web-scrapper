# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 19:44:21 2014

@author: tk
"""

import os
os.system('mkdir labor')
os.chdir(os.getcwd()+'/labor')
for i in range(0,100):
    os.system('mkdir work'+str(i))
    os.system('cp ../temp.py ./work'+str(i)+'/test.py')
    os.system('cp ../tk.sh ./work'+str(i)+'/tk.sh')
    os.chdir('work'+str(i))
    print os.getcwd()
    os.system('bash tk.sh '+str(i*10000)+' '+str(i*10000+10000))
    os.chdir('../')
#print os.system('nohup python '+'test.py '+str(i*100000)+' '+str(i*100000+100000)+' &')
#print os.chdir('../')
