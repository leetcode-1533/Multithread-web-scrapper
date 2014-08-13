# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 23:29:18 2014

@author: tk
"""

import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot
import csv 

page_info = pd.read_csv('page_info.csv')
field_li = pd.read_csv('field_li.csv')
field_info = pd.read_csv('field_info.csv')


page_info['pro_num'] = page_info['label']
#page_field = pd.merge()
field_merge = pd.merge(field_li,field_info,on='name',how='inner')

tk_merge = pd.merge(page_info,field_merge,on='pro_num',how='inner')

test1 =tk_merge[tk_merge['status']=='None']
test2 = tk_merge[tk_merge['status']=='Paid Back']
#print len(test2)
dic_fie = {}
for cat in tk_merge['name'].unique():
    print cat
    temp_wins1 = test1[test1['name'] == cat]
    temp_wins2 = test2[test2['name']==cat]
    temp_all = tk_merge[tk_merge['name']==cat]
    

    rate =  float(len(temp_wins1)+len(temp_wins2))/float(len(temp_all))
    dic_fie[cat] = rate
    
import matplotlib.pyplot as plt
D = dic_fie
#D = {u'Label1':26, u'Label2': 17, u'Label3':30}

plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())

plt.show()
#ax.set_xticklabels 

    
