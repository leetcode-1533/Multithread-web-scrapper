# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 17:20:11 2014

@author: tk
"""

import MySQLdb as mdb

def get_country(con,num):
    cur = con.cursor()
    cur.execute("select * from country_link where pro_num=\'"+str(num)+"\'")
    rows = cur.fetchall()
    target = rows[0][-1]
    cur.execute("select * from country_db where name=\'"+str(target)+"\'")
    country_rows = cur.fetchall()
    return country_rows[0]

def get_field(con,num):
    cur = con.cursor()
    cur.execute("select * from field_link where pro_num=\'"+str(num)+"\'")
    rows = cur.fetchall()
    target = rows[0][-1]
    cur.execute("select * from field_db where name=\'"+str(target)+"\'")
    field_rows = cur.fetchall()
    return field_rows[0]
    
def get_page(con,num):
        cur = con.cursor()
        cur.execute("select * from page_db where label=\'"+str(num)+"\'")
        rows = cur.fetchall()
        return rows[0]
            
if __name__ == "__main__":
    con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
    with con:
        cur = con.cursor()
        cur.execute("select label from page_db")
        rows = cur.fetchall()
        row_clip = rows[0:1000]
    van = []
    for item in row_clip:
        num = int(item[0])
        t1 = get_country(con,num)
        t2 = get_field(con,num)
        t3 = get_page(con,num)
        tm = t1+t2+t3     
        van.append(tm)
        
        

#    
#    t1 = get_country(330078)
#    t2 = get_field(330078)
#    t3 = get_page(330078)
#    tm = t1+t2+t3
#    
    

    
    
        
        
    
        
        
