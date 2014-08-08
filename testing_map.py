# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 16:11:30 2014

@author: tk
"""

import MySQLdb as mdb
import pandas.io.sql as psql

con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
df_mysql = psql.frame_query('select * from country_link',con = con)

