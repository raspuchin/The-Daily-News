#!/usr/bin/env python
# coding: utf-8
#
# @author : Sachin Pothukuchi
# you need : dailyNews.ini and vector.pickel
#

# In[1]:


import configparser
import json
import tweepy
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from scipy.sparse import coo_matrix
import pickle
import os
import nltk
import pandas as pd
nltk.download('stopwords')

nltk.download('wordnet')


# In[2]:


cv = None
tfidf_transformer = None
feature_names = None
stop_words = None

woeid = None
api = None


# In[3]:


def load():
    global stop_words
    global cv
    global tfidf_transformer
    global feature_names
    global woeid
    global api
    stop_words = set(stopwords.words("english"))
    new_words = ["using", "show", "result", "large", "also",
                 "iv", "one", "two", "new", "previously", "shown"]
    stop_words = stop_words.union(new_words)
    cv, tfidf_transformer, feature_names = pickle.load(
        open('vector.pickel', 'rb'))

    config = configparser.ConfigParser()

    config.read('dailyNews.ini')
    woeid = int(config['woeid']['woeid'])

    auth = tweepy.OAuthHandler(
        config['twitter_api']['api_key'], config['twitter_api']['api_secret'])
    auth.set_access_token(
        config['twitter_api']['token_key'], config['twitter_api']['token_secret'])
    api = tweepy.API(auth)


# In[4]:


def preprocess(articles):
    corp = []
    for text in articles:
        # Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', text)

        # Convert hashtags from camel case to normal text
        text = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text))

        # Convert to lowercase
        text = text.lower()

        # remove tags
        text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)

        # Convert to list from string
        text = text.split()

        # Stemming
        ps = PorterStemmer()
        # Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in stop_words]
        text = ' '.join(text)
        corp.append(text)
    return corp


# In[5]:


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


# In[6]:


def getKeywordList(article):
    corpus = preprocess([article])
    #print('Corpus: ' + corpus[0])
    tf_idf_vector = tfidf_transformer.transform(cv.transform(corpus))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(feature_names, sorted_items)
    return keywords


# In[7]:


def getTrends():
    global woeid
    global api
    trends = api.trends_place(woeid)
    trends = [x['name'] for x in trends[0]['trends']]
    trends = preprocess(trends)
    trends_final = []
    for trend in trends:
        if trend != '':
            trends_final.append(trend)
    return trends_final


# In[8]:


# returns 0 if no priority and 1 otherwise
def getPriority(article, trends):
    keywords = getKeywordList(article)
    for keyword in keywords:
        for trend in trends:
            if keyword in trends:
                return 1
    return 0


if __name__ == '__main__':
    load()
    art = input('Enter article: ')
    trends = getTrends()  # update trends every one hour?
    p = getPriority(art, trends)
    print(p)
