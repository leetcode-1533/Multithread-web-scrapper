# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 14:57:58 2014

@author: tk
"""

import folium
from pandas.stats.api import ols
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import requests
import json

#washing data
projects = pd.read_csv('projects.tsv',delimiter='\t')
goals = pd.read_csv('goals.tsv',delimiter='\t')
users = pd.read_csv('users.tsv',delimiter='\t')
backers = pd.read_csv('backers.tsv',delimiter='\t')


projects[['url','category','location']] = projects[['url','category','location']].astype(str)
projects = projects.dropna(how='any', subset=['start_date','end_date'])
projects[['start_date','end_date']] = projects[['start_date','end_date']].apply(pd.to_datetime)
locations = projects['location'].str.split(', ')
projects['city'] = locations.str[0]
projects['country'] = locations.str[-1]
booleans = locations.str[1] != locations.str[-1]
rows_with_states = locations[booleans].str[1]
projects['state'] = rows_with_states
projects['state'] = projects['state'].fillna('')

backers = backers.dropna(how='any')
backers['project']=backers['project'].astype(str)

backers_full = backers

backers_withmoney = backers[backers['amount'] != 'unknown']
backers_withmoney['amount']=backers_withmoney['amount'].astype(int)

# new direction to wash
goals = goals.dropna(how='any')
goals['url'] = goals['url'].astype(str)
goals['goal_amount']=goals['goal_amount'].astype(int)

#Merging dataset, uses Url to line up records
merged = pd.merge(goals,projects,on='url',how='inner')
projects['goal_amount'] = merged['goal_amount']
projects['sucessful']=1*projects['amount_raised']>projects['goal_amount']
projects['sucessful']=projects['sucessful'].astype(int)



mymap = folium.Map(location=[0,0],zoom_start=2)
data = projects
locations = json.load(open('indiegogo_geo.json'))

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



loc = data['location']
counts = loc.value_counts()
for test in loc.values:
    coordinates = get_locations(test)
    lat = coordinates['latitude']
    lon = coordinates['longitude']
    para = counts[test] * 50
    mymap.circle_marker(location=[lat,lon],radius = para,fill_color = '#f00')
    
    