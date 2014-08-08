# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 17:20:11 2014

@author: tk
"""

import MySQLdb as mdb

def get_country(num):
    con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
    with con:
        cur = con.cursor()
        cur.execute("select * from country_link where pro_num=\'"+str(num)+"\'")
        rows = cur.fetchall()
        target = rows[0][-1]
        cur.execute("select * from country_db where name=\'"+str(target)+"\'")
        country_rows = cur.fetchall()
        return country_rows[0]

def get_field(num):
    con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
    with con:
        cur = con.cursor()
        cur.execute("select * from field_link where pro_num=\'"+str(num)+"\'")
        rows = cur.fetchall()
        target = rows[0][-1]
        cur.execute("select * from field_db where name=\'"+str(target)+"\'")
        field_rows = cur.fetchall()
        return field_rows[0]
    
def get_page(num):
        con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
        with con:
            cur = con.cursor()
            cur.execute("select * from page_db where label=\'"+str(num)+"\'")
            rows = cur.fetchall()
            return rows[0]

    
    
        
        
    
        
        
