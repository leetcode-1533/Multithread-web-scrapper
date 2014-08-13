# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 16:11:30 2014

@author: tk
"""

import MySQLdb as mdb
import pandas.io.sql as psql
import json
import requests
import folium

con = mdb.connect('rosencrantz.berkeley.edu','kivalend','kivalend','kivalend')
df_mysql = psql.frame_query('select * from country_link',con = con)

locations = json.load(open('indiegogo/indiegogo_geo.json'))

def get_locations(loc1):
    if loc1 in locations:
        return locations[loc1]
    else:
        location_list = [loc1]
        postdata = {'locations':location_list}
        response = requests.post('http://rosencrantz.berkeley.edu:5555/geo',data=postdata)
        json_file =  json.loads(response.content)
        loc_lat_long = json_file['results'][0]
        return {'latitude':loc_lat_long['latitude'],'longitude':loc_lat_long['longitude']}
mymap = folium.Map(location=[0,0],zoom_start=2)
loc = df_mysql['name']
counts = loc.value_counts()
for test in loc.values:
    coordinates = get_locations(test)
    lat = coordinates['latitude']
    lon = coordinates['longitude']
    para = counts[test] * 50
    mymap.circle_marker(location=[lat,lon],radius = para,fill_color = '#f00')