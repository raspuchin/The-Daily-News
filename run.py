#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:41:04 2020

@author: nikhilmatta
"""

from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import data, getLinks, getArticleData
from model import loadModel, getSentiment, getSummary


HOST = 'localhost'
PORT = 27017
client = MongoClient(HOST, PORT)
database = client.dailyNews
articles = database.articlesData
j = 0


def storeArticles():
    for i in range(len(data['links'])):
        link = data['links'][i]
        category = data['category'][i]
        date = data['date'][i]
        image = data['image'][i]
        headline = data['headline'][i]
        article = data['article'][i]
        try:
            articleSummary = getSummary(data['article'][i])
            articleSentiment = getSentiment(data['headline'][i])
            articleData = {'link': link, 'category': category, 'date': date, 'image': image,
                           'headline': headline, 'article': article, 'summary': articleSummary, 'sentiment': articleSentiment}
            articles.update(articleData, articleData, upsert=True)
            print(j)
            j += 1
        except:
            pass


def clearLists():
    data['links'].clear()
    data['category'].clear()
    data['date'].clear()
    data['image'].clear()
    data['headline'].clear()
    data['article'].clear()
    data['summary'].clear()
    data['sentiment'].clear()


def scraperScheduler():
    getLinks()
    getArticleData()
    storeArticles()
    clearLists()


def startScheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(scraperScheduler, 'interval', hours=0.5)
    scheduler.start()


if __name__ == '__main__':
    loadModel()
    scraperScheduler()
    startScheduler()
