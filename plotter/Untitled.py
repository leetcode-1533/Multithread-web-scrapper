# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 11:02:41 2014

@author: tk
"""
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot
import numpy
import time
import datetime
#mpl.use('Agg')
#country_li = pd.read_csv('country_li.csv')
page_info = pd.read_csv('page_info.csv')
#field_info = pd.

#column adjustment..
page_info['Borrower_name'] = page_info['Currency_exchange_loss']
page_info['Currency_exchange_loss'] = page_info['Borrow_name']
page_info = page_info.drop('Borrow_name',1)

col = page_info['need_amount']
loc = page_info['location']
large_cat = page_info['large_cat']
#Washing “needed”
test = col.str.replace(',','')
tk = test.astype(float)

#washing repayment_term
uk = page_info['Repayment_Term'].str.replace('(more info)','')
tml = uk.str.replace('(','')
tmr = tml.str.replace(')','')
test_dh = tmr.str.replace('months','')
test_dh[test_dh==' ']=0
test_dh = test_dh.astype(int)
#pyplot.hist(test_dh,bins=15)
#washing list_date:
da = page_info['Listed_date']
#time_date = da.apply(lambda x: time.strptime(x,"%b %d, %Y"))
chall = []
new_da = da[0:63224]
new_da2=da[65722::]
da = pd.concat([new_da,new_da2])
x = [ datetime.datetime.strptime(test,"%b %d, %Y").date() for test in da]
y = range(len(x))

    

    
#list_date = pd.to_datetime(da)


#del_loc = numpy.where(repay==repay.max())[0][0]
#new_repay = numpy.delete(repay,del_loc)





#tk.hist(bins=100)


#axis_subplot = plotting_command()
#large_cat.value_counts().plot(kind='bar')
#mpl.pyplot.ylabel('ylabel')
#mpl.pyplot.xlabel('xaxis')
#mpl.pyplot.title('title')
#mpl.pyplot.tight_layout()
#
#figure = axis_subplot.get_figure()
#
#figure.savefig('test.png')
##mp


