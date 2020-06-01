#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:26:34 2020

@author: nikhilmatta
"""

from simpletransformers.classification import ClassificationModel
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig

sentimentModel = None
summarizerModel = None
tokenizer = None
summary = None
sentiment = None
arguments = None


def loadModel():
    global sentimentModel
    global summarizerModel
    global tokenizer
    global arguments
    arguments = {
        'silent': True
    }
    sentimentModel = ClassificationModel(
        'roberta', 'sentimentAnalysisModel', use_cuda=False, args=arguments)
    summarizerModel = BartForConditionalGeneration.from_pretrained(
        'bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('bart-large-cnn')


'''    
def getPrediction(text):
    global summary
    global sentiment
    text = [text]
    inputs = tokenizer.batch_encode_plus(text, max_length=1024, return_tensors='pt')
    summary_ids = summarizerModel.generate(inputs['input_ids'], num_beams=4, max_length=120, early_stopping=True)
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    sentiment = sentimentModel.predict(text)
    #print(str(prediction[0])+'\n'+str(summary[0]))
    #return (str(prediction[0]), str(summary[0]))
'''


def getSentiment(text):
    global sentiment
    text = [text]
    sentiment = sentimentModel.predict(text)
    return str(sentiment[0])


def getSummary(text):
    global summary
    text = [text]
    inputs = tokenizer.batch_encode_plus(
        text, max_length=1024, return_tensors='pt')
    summary_ids = summarizerModel.generate(
        inputs['input_ids'], num_beams=4, max_length=200, early_stopping=True)
    summary = [tokenizer.decode(g, skip_special_tokens=True,
                                clean_up_tokenization_spaces=False) for g in summary_ids]
    return str(summary[0])
