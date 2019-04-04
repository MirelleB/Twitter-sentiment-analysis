# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 18:11:35 2019

@author: Mirellebueno
"""



"""
Created on Sun Mar 31 12:40:03 2019

@author: Mirellebueno
"""


import nltk
nltk.download('stopwords')

import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict



class Models:

    

    def read_clean_dataset():
    
        dataset = pd.read_csv('Tweets_Mg.csv',encoding='utf-8')


        dataset.count()
        ## clean the dataset
        dataset['Text'].str.lower()
        
        dataset['Text'].replace(['^a-zA-Z0-9ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïðòóôõöùúûüýÿ,!?\'\`\.\(\)'],[""],regex=True)
        dataset['Text'].replace(['INC[0-9]{7,}'],[" <INCIDENTE> "],regex=True)
        dataset['Text'].replace(['[+-]?\d+(?:\.\d+)?'],[" <NUMERO> "],regex=True)
        dataset['Text'].replace(['!'],[" ! "],regex=True)
        dataset['Text'].replace(['\('],[" ( "],regex=True)
        dataset['Text'].replace(['\)'],[" ) "],regex=True)
        dataset['Text'].replace(['\?'],[" ? "],regex=True)
        dataset['Text'].replace(['\s{2,}'],[" "],regex=True)
        dataset['Text'].replace("..","")
        dataset['Text'].replace('"', "")
        dataset['Text'].replace("''", "")
        dataset['Text'].replace("p/", "")
        dataset['Text'].replace("RT ", "")
    
        return dataset    
 


    def predict(new_twitter):
        
        train_dataset=Models.read_clean_dataset()
        twitter_train=train_dataset["Text"].values
        target = train_dataset["Classificacao"].values
        stopwords = nltk.corpus.stopwords.words('portuguese')
         ##Remove the stop Words
         
         
        #Vectorize the words 
        vectorizer = CountVectorizer(ngram_range = (1, 2),stop_words=stopwords)
        freq_tweets = vectorizer.fit_transform(twitter_train)

        model = MultinomialNB()
        model.fit(freq_tweets, target)
       
    
        freq_test = vectorizer.transform(new_twitter)
        results=model.predict(freq_test)
        #print("concuit")
        return results









