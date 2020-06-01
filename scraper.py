#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:11:14 2020

@author: nikhilmatta
"""

import requests
from bs4 import BeautifulSoup
import re

data = {'links': [], 'headline': [], 'image': [], 'category': [],
        'date': [], 'article': [], 'summary': [], 'sentiment': []}
#df = pd.DataFrame(columns = ['links','image','category','date','article','summary','sentiment'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15.3; rv:42.0) Gecko/20100101 Firefox/28.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}


def getLinks():
    for i in range(5, 2, -1):
        try:
            r = requests.get(
                'https://www.hindustantimes.com/latest-news/?pageno='+str(i), headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            try:
                for url in soup.findAll("a", {"title": "read more"}):
                    if url['href'] not in data['links']:
                        data['links'].insert(i, url["href"])
            except:
                pass
        except:
            pass


def getArticleData():
    for i in range(len(data['links'])):
        try:
            r = requests.get(data["links"][i], headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            try:
                data['headline'].insert(i, soup.find("h1").getText())
            except:
                data['headline'].insert(i, "-")
            try:
                data['category'].insert(i, soup.find(
                    "span", {"class": "cta-link lok-sabha-elections-cb-sectionmr-15"}).getText())
            except:
                data['category'].insert(i, "-")
            try:
                data['date'].insert(i, soup.find(
                    "span", {"class": "text-dt"}).getText())
            except:
                data['date'].insert(i, "-")
            try:
                data['image'].insert(i, soup.find("figure").find(
                    'img', {'src': re.compile('.jpg')}).get('src'))
            except AttributeError:
                try:
                    data['image'].insert(i, soup.find("figure").find(
                        'img', {'src': re.compile('.png')}).get('src'))
                except AttributeError:
                    try:
                        data['image'].insert(i, soup.find("figure").find(
                            'img', {'src': re.compile('.JPG')}).get('src'))
                    except AttributeError:
                        try:
                            data['image'].insert(i, soup.find("figure").find(
                                'img', {'src': re.compile('.PNG')}).get('src'))
                        except:
                            try:
                                data['image'].insert(i, soup.find("figure").find(
                                    'img', {'src': re.compile('.jpeg')}).get('src'))
                            except:
                                data['image'].insert(i, "-")
            txt = ""
            try:
                for s in soup.find("div", {"class": "storyDetail"}).findAll("p"):
                    txt = txt+s.getText()
                # print(txt)
                data['article'].insert(i, str(txt))
            except:
                data['article'].insert(i, "-")
        except:
            pass

# df=pd.DataFrame.from_dict(data)
