# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 17:27:57 2014

@author: tk
"""
import requests
from bs4 import BeautifulSoup
#import csv
import MySQLdb
import re
import sys
#To identify if the image is the default image
#import Image
#import urllib, cStringIO
#import numpy



#def parse_contributor(num):
#    url = "http://www.kiva.org/ajax/callLoan_TopLendingTeamSubView?&show_all_teams=1&includeCssAndJs=0&biz_id={0}".format(num)
#    data_dict = {}
#    response = requests.get(url)   
#    sc = response.status_code
#    html = response.content
#    soup = BeautifulSoup(html)     
#    p_container = soup.find('ul',{'class':'teamCards'})
#    if p_container is None:
#        # data_dict['cor_team']=[]
#        return data_dict
#    else:
#        temp_list = []
#        for container in p_container.findAll('li'):
#            temp = {}
#            img_url =  container.find('img')['src']
#            if img_url.endswith('default_team.png'):
#                img_url = ''
#            cor_title_1 = container.find('h1')
#            cor_name  = cor_title_1.find('a').text
#            
#            temp['cor_team_img']=img_url
#            temp['cor_team_name']=cor_name
#            temp_list.append(temp)
#        # data_dict['cor_team']=temp_list
#        return data_dict
#         
def parse_country(soup,num):
        countrydict = {}
        countrydata=soup.findAll('ul',{'class':'countryMapStatsGrid'})
        if countrydata is None:
            raise ValueError
        else :
            countrydata=soup.find('ul',{'class':'countryMapStatsGrid'})

        numbers=countrydata.findAll('div',{'class':'number_sans'})
        
        # average income
        number1 = numbers[0].text.strip()
        number1 = str(number1)
        if len(number1)>=1:
            number1 = filter(lambda ch:ch in '0123456789.', number1)
            countrydict['country_income'] = number1
        else:
            countrydict['country_income'] = 0 
        
        # loans fundraising
        number2 = numbers[1].text.strip()
        number2 = str(number2)
        if len(number2)>=1:
            number2 = filter(lambda ch:ch in '0123456789.', number2)
            countrydict['country_loans_items'] = number2
        else:
            countrydict['country_loans_items'] = 'NaN' 
  
        # funds lent
        number3 = numbers[2].text.strip()
        number3 = str(number3)
        if len(number3)>=1:
            number3 = filter(lambda ch:ch in '0123456789.', number3)
            countrydict['country_loans_amounts'] = number3
        else:
            countrydict['country_loans_amounts'] = 'NaN'
 
        # rate
        number4 = numbers[3].text.strip()
        number4 = str(number4)
        if len(number4)<1:
            countrydict['country_exchange'] = 'NaN'
        elif number4=='US Dollars':
            countrydict['country_exchange'] = 1
        else:
            number4 = filter(lambda ch:ch in '0123456789.', number4)
            countrydict['country_exchange'] = number4                
        div_tag1 = soup.find('div',{'class':'wrap'})
        div_tag2 = div_tag1.find('div',{'class': 'mainWrapper container'})
        div_tag3 = div_tag2.find('div',{'class': 'main'})
        lists = div_tag3.findAll('div',{'id': 'loanProfileTabs'})
        if lists == []:
            return []
        header_tag = div_tag2.find('div', {'id': 'pageHeader'})
        div_meta = header_tag.find('div',{'class': 'meta'})
        locccc = div_meta.find('a').text.strip()
        country_name = locccc.split(',')[-1]
        countrydict['country_name'] = country_name
        return countrydict 

def parse_page(soup,num):
    camp = {}       
    div_tag1 = soup.find('div',{'class':'wrap'})
    div_tag2 = div_tag1.find('div',{'class': 'mainWrapper container'})
    div_tag3 = div_tag2.find('div',{'class': 'main'})
    lists = div_tag3.findAll('div',{'id': 'loanProfileTabs'})
    if lists == []:
        return
    div_tag4 = lists[0]
    sect_tag = div_tag4.find('section',{'id': 'businessProfile'})
    header_tag = div_tag2.find('div', {'id': 'pageHeader'})
    campppp = header_tag.find('h2').text
    camp['borrower_name'] = filter(lambda ch:ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ', campppp)
    div_meta = header_tag.find('div',{'class': 'meta'})
    locccc = div_meta.find('a').text.strip()
    camp['location'] = locccc
    camp['large_sector'] = div_meta.find('span',{'class':'sector'}).text.strip()
    camp['specific_sector'] = div_meta.find('span',{'class': 'activity'}).text.strip()
    div_tag8 = sect_tag.find('div',{'class': 'g4 z'})
    need_text = div_tag8.find('div',{'class': 'loanExcerpt'}).text.strip()
    t1_find = re.findall('\$.*\040',need_text)[0]
    t2_find = re.findall('[-+]?[0-9]*\,?[0-9]+',t1_find[1:])[0]  
    camp['needed_amount'] = t2_find
  
    dl_repay = div_tag8.find('dl')
    dds = dl_repay.findAll('dd')
    tt = dds[0].text.split(' ')
    camp['repayment term'] = tt[0]+' '+tt[1]
    camp['repayment schedule'] = dds[1].text.strip()
    camp['pre-disbursed_date'] = dds[2].text.strip()
    camp['listed_date'] = dds[3].text.strip()
    camp['currency exchange loss'] = dds[4].text.strip()
    stat_tag = div_tag8.findAll('div',{'class': 'loanStatus notice'})
    if stat_tag != []:
        camp['status'] = stat_tag[0].text.strip()
    else:
        camp['status'] = 'none'
    #tring to find pic_url:
    url = soup.find('figure',{'class':'businessFig'}).find('a')['href']
#    file_img = cStringIO.StringIO(urllib.urlopen(url).read())
#    img1 = Image.open(file_img)
#    img2 = Image.open('temp.jgp')
#    code = is_unuploded_pic(img1,img2)
#    if code == 0:
#        url = "Not uploaded"
    camp['url']=url 
    
    #trying to find tags: 
    tag_list = []
    try:
        tag_par = soup.find('section',{'id':'loanTags'})
        tag_list_html = tag_par.findAll('a')
        for item in tag_list_html:
            tag_list.append(item.text)
    except AttributeError:
        pass
    camp['tag_list'] = tag_list  
    return camp
def tag_convert(tag_list):
    string = ""
    for item in tag_list:
        string += item
    return string
        
    
def is_unuploded_pic(img1,img2):
    if img1.size != img2.size or img1.getbands() != img2.getbands():
        return -1
    s = 0
    for band_index, band in enumerate(img1.getbands()):
        m1 = numpy.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
        m2 = numpy.array([p[band_index] for p in img2.getdata()]).reshape(*img2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s
    
def parse_field(soup,num):
    camp = {}
    div_tag1 = soup.find('div',{'class':'wrap'})
    div_tag2 = div_tag1.find('div',{'class': 'mainWrapper container'})
    div_tag3 = div_tag2.find('div',{'class': 'main'})
    lists = div_tag3.findAll('div',{'id': 'loanProfileTabs'})
    if lists == []:
        raise ValueError
    div_tag4 = lists[0]
    sect_tag = div_tag4.find('section',{'id': 'businessProfile'})
    div_tag5 = sect_tag.find('div',{'class': 'g4 z'})
    asd_tag = div_tag5.find('aside', {'class': 'partnerSummary statsBox'})
    div_tag6 = asd_tag.find('div', {'class': 'info'})
    dl_tag = div_tag6.find('dl')
    dd_tags = dl_tag.findAll('dd')
    nameeee = dd_tags[0].text.strip()
    camp['name'] = filter(lambda ch:ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ', nameeee)
    camp['due_diligence_type'] = dd_tags[1].text.strip()
    div = dd_tags[2].find('div')
    try:
        risk_rating = re.findall("\d+.\d+",div['title'])[0]
        camp['risk_rating'] = risk_rating
    except IndexError:
        try:
            risk_rating = re.findall('\d',div['title'])[0]
            camp['risk_rating'] = risk_rating
        except IndexError:
            camp['risk_rating'] = None
    camp['time_on_kiva'] = dd_tags[3].text.strip()
    camp['Kiva_borrowers'] = dd_tags[4].text.strip()
    camp['total_loans'] = dd_tags[5].text.strip()
    camp['interest_and_fees_are_charged'] = dd_tags[6].text.strip()
    camp['portfolio_yield'] = dd_tags[7].text.strip()
    camp['profitability'] = dd_tags[8].text.strip()
    camp['average_loan_siza'] = dd_tags[9].text.strip()
    camp['deliquency_rate'] = dd_tags[10].text.strip()
    camp['loans_at_risk_rate'] = dd_tags[11].text.strip()
    camp['default_rate'] = dd_tags[12].text.strip()
    camp['currency_exchange_loss_rate'] = dd_tags[13].text.strip()
    return camp

#def combiner(num):
#    temp = {}
#    test1 = parse_contributor(num)
#    test2 = parse_Country(num)
#    test3 = parse_page(num)
#    test4 = parse_field(num)
#    temp.update(test1)
#    temp.update(test2)
#    temp.update(test3)
#    temp.update(test4)
#    return temp
#    
#def writer(mother_list,keys):    
#    with open('spreadsheet7398.csv','w') as outfile:
#        writer = csv.DictWriter(outfile,keys)
#        writer.writeheader()
#        writer.writerows(mother_list)
#    
#def writer_sol(num):
#    writer = csv.writer(open(str(num),'wb'))
#    cd_dict = parse_Country(num)
#    for key, value in cd_dict.items():
#        writer.writerow([key,value])
##    db = MySQLdb.connect(host='rosencrantz.berkeley.edu',user='kivalend',passwd='kivalend')
##    cursor = db.cursor()

def create_page_db(db,cur,num,soup):
    try:
        create_page_str = 'create table page_db (label float primary key unique,borrower_name varchar(30),currency_exchange_loss varchar(30),large_sector varchar(30),listed_date varchar(30),location varchar(30),need_amount float,pre_disbursed_date varchar(30),repayment_schedule varchar(30),repayment_term varchar(30),specific_sector varchar(30),status varchar(30),tag_list varchar(300),url varchar(50))'
        cur.execute(create_page_str)
    except MySQLdb.OperationalError:
        try:
            dic = parse_page(soup,num)
            insert_str = "insert into page_db (label,borrower_name,currency_exchange_loss,large_sector,listed_date,location,need_amount,pre_disbursed_date,repayment_schedule,repayment_term,specific_sector,status,tag_list,url) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\')"
            tk_str = insert_str.format(num,dic['borrower_name'],dic['currency exchange loss'],dic['large_sector'],dic['listed_date'],dic['location'],dic['needed_amount'],dic['pre-disbursed_date'],dic['repayment schedule'],dic['repayment term'],dic['specific_sector'],dic['status'],tag_convert(dic['tag_list']),dic['url'])
            cur.execute(tk_str)
            db.commit()
        except MySQLdb.IntegrityError:
            pass       
    
def create_field_db(db,cur,num,soup):
    try:
        create_field_str = 'create table field_db (kiva_borrowers varchar(30),average_loan_size varchar(30),currency_exchange_loss_rate varchar(30),default_rate varchar(30), deliquency_rate varchar(30),due_diligence_type varchar(30),interest_and_fees_are_chared varchar(30),loans_at_risk_rate varchar(30),name varchar(30) primary key unique,portfolio_yield varchar(30),profitability varchar(30),risk_rating varchar(30),time_on_kiva varchar(30),total_loans varchar(30))'
        create_link_str = 'create table field_link(pro_num float unique, name varchar(30) unique, foreign key(pro_num) references page_db(label) on delete cascade ON UPDATE CASCADE, foreign key(name) references field_db(name) on delete cascade ON UPDATE CASCADE)'
        cur.execute(create_field_str)
        cur.execute(create_link_str)
    except MySQLdb.OperationalError:
        try:
            dic = parse_field(soup,num)
            insert_str = "insert into field_db (kiva_borrowers,average_loan_size,currency_exchange_loss_rate,default_rate,deliquency_rate,due_diligence_type,interest_and_fees_are_chared,loans_at_risk_rate,name,portfolio_yield,profitability,risk_rating,time_on_kiva,total_loans) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\',\'{13}\')".format(dic['Kiva_borrowers'],dic['average_loan_siza'],dic['currency_exchange_loss_rate'],dic['default_rate'],dic['deliquency_rate'],dic['due_diligence_type'],dic['interest_and_fees_are_charged'],dic['loans_at_risk_rate'],dic['name'],dic['portfolio_yield'],dic['profitability'],dic['risk_rating'],dic['time_on_kiva'],dic['total_loans'])
            cur.execute(insert_str)
            insert_link = "insert into field_link (pro_num,name) values (\'{0}\',\'{1}\')"
            insert_act = insert_link.format(num,dic['name'])
            cur.execute(insert_act)
        except MySQLdb.IntegrityError:
            try:
                insert_link = "insert into field_link (pro_num,name) values (\'{0}\',\'{1}\')"
                insert_act = insert_link.format(num,dic['name'])
                cur.execute(insert_act)
            except MySQLdb.IntegrityError:
                pass
        finally:
            db.commit()
            

def create_country_db(db,cur,num,soup):        
    try:       
        create_country_str = "create table country_db (name varchar(30) primary key unique,loans_item float, income float, loans_amounts float, exchange float)"
        cur.execute(create_country_str)
        create_link_str = 'create table country_link (pro_num float unique, name varchar(30) unique, foreign key(pro_num) references page_db(label) on delete cascade ON UPDATE CASCADE, foreign key(name) references country_db(name) on delete cascade ON UPDATE CASCADE)'
        cur.execute(create_link_str)
    except MySQLdb.OperationalError:
        try:        
            dic = parse_country(soup,num)
            insert_cou_str = 'insert into country_db (name,loans_item,income,loans_amounts,exchange) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\')'
            inserted = insert_cou_str.format(dic['country_name'],dic['country_loans_items'],dic['country_income'],dic['country_loans_amounts'],dic['country_exchange'])
            cur.execute(inserted)
            insert_link = "insert into country_link (pro_num,name) values (\'{0}\',\'{1}\')"
            insert_act = insert_link.format(num,dic['country_name'])
            cur.execute(insert_act)
        except MySQLdb.IntegrityError:
            try:
                insert_link = "insert into country_link (pro_num,name) values (\'{0}\',\'{1}\')"
                insert_act = insert_link.format(num,dic['country_name'])
                cur.execute(insert_act)
            except MySQLdb.IntegrityError:
                pass
        finally:
            db.commit()

                                                        
if __name__ == "__main__":
#    pass
    db = MySQLdb.connect(host='localhost',user='root',passwd='root',db='kivalend',unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock')
    cur = db.cursor()
    for i in range(500001,399999,-1):
        try:
            url = "http://www.kiva.org/lend/{0}".format(i)
            res = requests.get(url)
            if res.status_code != 200 or res.history != []:
                print "not 200" + url
            else:
                print "start at{0}".format(i)
                html = res.content
                soup = BeautifulSoup(html)
                create_page_db(db,cur,i,soup)
                create_country_db(db,cur,i,soup)
                create_field_db(db,cur,i,soup)
                print "finish at{0}".format(i)
        except MySQLdb.IntegrityError:
            continue
        
            
            
    

        
    


        

        



    
    

    
        
        
