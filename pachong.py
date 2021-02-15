import requests    #网络请求
import re 
import time        #时间模块
import json
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from urllib.parse import quote
import traceback
from datetime import datetime,timedelta
import csv
import os
from time import sleep
import binascii
import base64
import urllib.request
import urllib
import re
import rsa

from cookie import Prelogin
from cookie import PostData
from cookie import RSAEncoder

class Pach():
    
    def __init__(self,keyword:str,headers,starttime,endtime,filepath:str):
        self.headers = headers
        self.keyword = keyword
        self.starttime = starttime
        self.endtime = endtime
        self.filepath = filepath
        
        
    def get_text(self,url):
        try:
            self.obtain_headers()
            res = requests.get(url,headers = self.headers)
            ret = res.content
            soup = BeautifulSoup(ret,'lxml')
            return soup
        except Exception as e:
            print('Error:',e)          
            
            
    #判断是否已经存在csv       
    def create_csv(self):
        try:
            if os.path.isfile(self.filepath) == True:
                pass
            else:
                with open(self.filepath,'a',encoding = 'utf-8-sig',newline = '') as f:
                    pass
        except Exception as e:
            print('Error:',e)
           
    
    #写入csv文件       
    def write_csv(self,comment,time1):
        try:
            with open(self.filepath,'r',encoding='utf-8-sig',newline='') as f:
                line = f.readlines()
                l = len(line)
            
            with open(self.filepath,'a+',encoding='utf-8-sig',newline='') as f:
                fieldname = ['发布时间','发布内容']
                if l == 0:
                    writer = csv.DictWriter(f,fieldnames=fieldname)
                    writer.writeheader()
                    for i in range(int(len(time1))): 
                        if comment[i] != []:
                            writer.writerow([time1[i]]+[comment[i]])
                            writer.writerow({'发布时间':time1[i],'发布内容':comment[i]})
                    
                else:
                    writer = csv.writer(f)
                    for i in range(int(len(time1))):
                        if comment[i] != []:
                            writer.writerow([time1[i]]+[comment[i]])
        except Exception as e:
            print('Error:',e)




class Pacn(Pach):
    
    #根据时间和关键词获得url    
    def get_url(self,starttime,endtime,page):
        url0 = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword='
        keywords = quote(self.keyword)
        url1 = '&advancedfilter=1&'
        url2 = 'starttime=' + str(starttime) +'&'
        url3 = 'endtime=' + str(endtime) +'&'
        url4 = 'sort=time&page='
        url5 = str(page)
        url = url0 + keywords + url1  + url2 + url3 + url4 + url5
        print(url)
        return url
    
    def obtain_headers(self):
        pass
     
    def get_comment(self,info):
        try:
            final_text = []
            div = info.body.find_all("span",class_="ctt")
            for i in div:
                final_text.append(i.text)
            return final_text
        except Exception as e:
            print('Error:',e)
            
        
    #获取发布时间
    def get_publish_time(self,info):
        try:
            final_time = []
            str_time = info.body.find_all("span",class_="ct")
            for i in str_time:
                print(i.text.split('\xa0'))
                publish_time = i.text.split('\xa0')[0]
                if '刚刚' in publish_time:
                    publish_time = datetime.now().strftime('%Y-%m-%d% H:%M')
                elif '分钟' in publish_time:
                    minute = publish_time[:publish_time.find('分钟')]
                    minute = timedelta(minutes=int(minute))
                    publish_time = (datetime.now() - minute).strftime('%Y-%m-%d% H:%M')
                elif '今天' in publish_time:
                    today = datetime.now().strftime('%Y-%m-%d')
                    time = publish_time[3:]
                    publish_time = today + ' ' + time
                elif '月' in publish_time:
                    year = datetime.now().strftime('%Y')
                    month = publish_time[0:2]
                    day = publish_time[3:5]
                    time = publish_time[7:12]
                    publish_time = year + '-' + month + '-' + day + ' ' + time
                final_time.append(publish_time)
            print(final_time)
            return final_time
        except Exception as e:
            print('Error:',e)
            
        #运行爬虫
    def run(self):
        endtime_final = self.count_endtime()
        for i in endtime_final:
            time.sleep(10)
            print(i)
            for j in range(101):
                print(j)
                url = self.get_url(i,i,j)
                text = self.get_text(url)
                comment = self.get_comment(text)
                publish_time = self.get_publish_time(text)
                if publish_time == []:
                    break
                else:
                    self.create_csv()
                    self.write_csv(comment,publish_time)
            
    def count_endtime(self):
        endtime_final = []
        #将输入的转化为事件类型计算间隔天数
        stime = str(self.starttime)
        etime = str(self.endtime)
        stime = stime[0:4]+'-'+stime[4:6]+'-'+stime[6:]
        etime = etime[0:4]+'-'+etime[4:6]+'-'+etime[6:]
        
        start = time.mktime(time.strptime(stime,'%Y-%m-%d'))
        end = time.mktime(time.strptime(etime,'%Y-%m-%d'))
        #间隔天数计算方式
        count_days = int((end - start)/(24*60*60))
        #将结束日转化为日期类型
        endtime_ = datetime.strptime(etime,'%Y-%m-%d')
        #迭代算出以一天为步的时间迭代
        for i in range(count_days+1):
            offset = timedelta(days=-i)
            #将事件类型转化为可输入爬取的int类型
            end_time = (endtime_+ offset).strftime('%Y-%m-%d')
            end_time = str(end_time)
            end_time = int(end_time[0:4]+end_time[5:7]+end_time[8:])
            endtime_final.append(end_time)
        return endtime_final

    

class Pacom(Pach):
    
    def __init__(self,keyword:str,headers,starttime,endtime,filepath:str,username:str,password:str):
        self.keyword = keyword
        self.starttime = starttime
        self.endtime = endtime
        self.filepath = filepath
        self.username = username
        self.password = password
        self.login_url = r'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'  #noqa
        self.prelogin_url = r'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.15)'  #noqa
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'  #noqa
        }
    
    def login(self):
        pubkey, servertime, nonce, rsakv = Prelogin(self.prelogin_url)
        post_data = PostData(self.username, self.password, pubkey, servertime,
                             nonce, rsakv)
        session = requests.Session()
        response = session.post(self.login_url, params=post_data,
                                headers=self.header)

        text = response.content.decode('gbk')
        pa = re.compile(r'location\.replace\(\'(.*?)\'\)')
        redirect_url = pa.search(text).group(1)
        response = session.get(redirect_url, headers=self.header)
        return session.cookies
    
    def obtain_headers(self):
        cookie = self.login()
        dict1=requests.utils.dict_from_cookiejar(cookie)
        a = ''
        for i in range(13):
            if i != 12:
                a += str(list(dict1.items())[i][0]) + '=' +str(list(dict1.items())[i][1])+';'
            else:
                a += str(list(dict1.items())[i][0]) + '=' +str(list(dict1.items())[i][1])
        self.headers = {
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
                        'cookie':str(a)
                        }
        
        
    #根据时间和关键词获得url    
    def get_url(self,starttime,endtime,page):
        url0 = 'https://s.weibo.com/weibo/?q='
        keywords = quote(self.keyword)
        url1 = '&typeall=1&suball=1&timescope=custom:'
        url2 = str(starttime) 
        url3 = ':' + str(endtime)
        url4 = '&Refer=g'
        if int(page) > 1:
            url5 = '&page='+str(page)
            url = url0 + keywords + url1  + url2 + url3 + url4 + url5
        else:
            url = url0 + keywords + url1  + url2 + url3 + url4
        print(url)
        return url
    
    def get_comment(self,info):
        try:
            final_text = []
            div = info.body.find_all("div",class_="content")       
            for i in div:
                t = i.find('p',class_='txt')
                b=''
                for word in t.text:
                    if word != ' ' and word != '\n':
                        b+=word
                final_text.append(b)
            print(len(final_text))
            return final_text
        except Exception as e:
            print('Error:',e)
            
    #获取发布时间
    def get_publish_time(self,info):
        try:
            final_time = []
            str_time = info.body.find_all("div",class_="content")
            for i in str_time:
                t = i.find_all("p",class_="from")
                t = t[-1]
                b=''
                for word in t.text:
                    if word != ' ' and word != '\n':
                        b += word
                publish_time = b.split('\xa0')[0]
                print(publish_time)
                if '刚刚' in publish_time:
                    publish_time = datetime.now().strftime('%Y-%m-%d% H:%M')
                elif '分钟' in publish_time:
                    minute = publish_time[:publish_time.find('分钟')]
                    minute = timedelta(minutes=int(minute))
                    publish_time = (datetime.now() - minute).strftime('%Y-%m-%d% H:%M')
                elif '今天' in publish_time:
                    today = datetime.now().strftime('%Y-%m-%d')
                    time = publish_time[3:]
                    publish_time = today + ' ' + time
                elif '月' in publish_time:
                    year = datetime.now().strftime('%Y')
                    month = publish_time[0:2]
                    day = publish_time[3:5]
                    time = publish_time[6:11]
                    publish_time = year + '-' + month + '-' + day + ' ' + time
                final_time.append(publish_time[0:10])
            return final_time
        except Exception as e:
            print('Error:',e)
            
    def count_endtime(self):
        endtime_final = []
        #将输入的转化为事件类型计算间隔天数
        stime = str(self.starttime)
        etime = str(self.endtime)
        stime = stime[0:4]+'-'+stime[4:6]+'-'+stime[6:]
        etime = etime[0:4]+'-'+etime[4:6]+'-'+etime[6:]
        
        start = time.mktime(time.strptime(stime,'%Y-%m-%d'))
        end = time.mktime(time.strptime(etime,'%Y-%m-%d'))
        #间隔天数计算方式
        count_days = int((end - start)/(24*60*60))
        #将结束日转化为日期类型
        endtime_ = datetime.strptime(etime,'%Y-%m-%d')
        #迭代算出以一小时为步的时间迭代
        for i in range(count_days+1):
            offset = timedelta(days=-i)
            #将事件类型转化为可输入爬取的int类型
            end_time = (endtime_+ offset).strftime('%Y-%m-%d')
            for j in range(24):
                end_time1 = str(end_time)
                end_time1 = end_time1[0:4]+'-'+end_time1[5:7]+'-'+end_time1[8:]+'-'+str(j)
                endtime_final.append(end_time1)
        return endtime_final
    
        #运行爬虫
    def run(self):
        endtime_final = self.count_endtime()
        for i in range(len(endtime_final)-1):
            e1 = endtime_final[i]
            e2 = endtime_final[i+1]
            for j in range(50):
                print(j)
                time.sleep(5)
                url = self.get_url(e1,e2,j)
                text = self.get_text(url)
                comment = self.get_comment(text)
                publish_time = self.get_publish_time(text)
                if publish_time == []:
                    break
                else:
                    self.create_csv()
                    self.write_csv(comment,publish_time)

    
    
'''
headers = {
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    'cookie' : 'ALF=1594803672; SCF=AvKkxfCkQJ6Biv6ovBZmEQTucJOUdeUUQaP1QT1DzLr2AjZHRaqTQXpY1JPpt5iLF1oG1AS8RJJLox6aMqHr-p4.; SUHB=0S7C0yBI9wZgU2; _T_WM=19966017200; SUB=_2A25z7xdRDeRhGeNI4lIS9CzEyzmIHXVRE7kZrDV6PUJbkdAKLRT3kW1NSAqo3lYY96VQ5fuisox-miJqXDQZ8UMP'
}
pachong = Pacn('瑞幸',headers,20200622,20200622,'pachong.csv')
pachong.run()
''' 
