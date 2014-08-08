# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 17:20:11 2014

@author: tk
"""
import temp
import MySQLdb as mdb
import csv
import requests
from bs4 import BeautifulSoup

def get_country(num):
        con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
        cur = con.cursor()
        cur.execute("select * from country_link where pro_num=\'"+str(num)+"\'")
        rows = cur.fetchall()
        target = rows[0][-1]
        cur.execute("select * from country_db where name=\'"+str(target)+"\'")
        country_rows = cur.fetchall()
        con.close()
        return country_rows[0]

def get_field(num):
    con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
    cur = con.cursor()
    cur.execute("select * from field_link where pro_num=\'"+str(num)+"\'")
    rows = cur.fetchall()
    target = rows[0][-1]
    cur.execute("select * from field_db where name=\'"+str(target)+"\'")
    field_rows = cur.fetchall()
    con.close()
    return field_rows[0]
    
def get_page(num):
        con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
        cur = con.cursor()
        cur.execute("select * from page_db where label=\'"+str(num)+"\'")
        rows = cur.fetchall()
        con.close()
        return rows[0]
        
def writer(mother_list):
    #get a sample of dict
    url = "http://www.kiva.org/lend/{0}".format(700050)
    res = requests.get(url)
    soup = BeautifulSoup(res.content)
    page_sample= temp.parse_page(soup,700050)
    field_sample = temp.parse_field(soup,700050)
    country_sample = temp.parse_country(soup,700050) 
    
    with open('file_tk.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(country_sample.keys()+field_sample.keys()+page_sample.keys())
        for row in mother_list:
            csv_out.writerow(row)
                
if __name__ == "__main__":
    con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
    with con:
        cur = con.cursor()
        cur.execute("select label from page_db")
        rows = cur.fetchall()
        print len(rows)
    van = []
    for item in rows:
        num = int(item[0])
        t1 = get_country(num)
        t2 = get_field(num)
        t3 = get_page(num)
        tm = t1+t2+t3     
        van.append(tm)
    writer(van)
    
        

#    
#    t1 = get_country(330078)
#    t2 = get_field(330078)
#    t3 = get_page(330078)
#    tm = t1+t2+t3
#    
    

    
    
        
        
    
        
        
