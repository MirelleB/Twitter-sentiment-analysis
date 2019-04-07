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
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier



class Models:
    

    def __init__(self):
        
        print("INICIALIZANDO")
        train_dataset=Models.read_clean_dataset()
        
        twitter_train=train_dataset["Text"].values
        
        target =train_dataset["Classificacao"].values
        stopwords = nltk.corpus.stopwords.words('portuguese')
        
        print("REtirei stop words")
         
        #Vectorize the words 
        self.vectorizer = CountVectorizer(ngram_range = (1, 2),stop_words=stopwords)
        freq_tweets = self.vectorizer.fit_transform(twitter_train)
        
        print("OBTIVE FREQUENCIA")
        
        self.modelNB = MultinomialNB()
        self.modelNB.fit(freq_tweets, target)
        
        print("TERMINEI")
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
 


    def predict(self,new_twitter):
        print("ENTREI NO PREDICT")
    
        freq_test = self.vectorizer.transform(new_twitter)
        
        y_predict_NB=self.modelNB.predict(freq_test)
       
        #print("concuit")
        return y_predict_NB









