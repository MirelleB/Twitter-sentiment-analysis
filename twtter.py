# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:35:04 2019

@author: Mirellebueno
"""

import json
import tweepy

from flask import Flask, render_template
import numpy as np
import class_modelo
import os
import re
from flask_socketio import SocketIO

consumer_key = 'TW9Jd0pnZll4NUrVGsKDu7hdc'
consumer_secret = 'YOlIsFvjioIZ4ZOe2VxHmnKmDOfed3rXvGktpseEeAdY6ScN0v'
access_token = '2666103462-34DtnGcugMlXiTe2eBfvKn3NcqtKtjtk4E0nwIk'
access_token_secret = '881rNts3uPn11xfNLDrach4gpC6INgsklY76KfIausmfM'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

consulta = "Iphone"
app = Flask(__name__)
socketio = SocketIO(app)
 
#Variável que irá armazenar todos os Tweets com a palavra escolhida na função search da API
#Coletando tweets
class CustomStreamListener(tweepy.StreamListener):
 
  def on_status(self, tweet):
    #Quando receber algum status, esta função pode manipular o objeto tweet. Exemplos:
    print(tweet.author.screen_name)
    #print(tweet.text.encode('utf-8'))
    
    train_dataset=class_modelo.Models.leitura_limpeza_arquivo()

    tweets =train_dataset["Text"].values
    classes = train_dataset["Classificacao"].values

    teste=[]
    
   
    #expressao=re.compile(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)')
  
    twitter_clean=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
    twitter_clean=twitter_clean.replace('RT', '')
    twitter_clean=twitter_clean.replace("..","")
    twitter_clean=twitter_clean.replace('"', "")
    twitter_clean=twitter_clean.replace("''", "")
    twitter_clean=twitter_clean.replace("p/", "")
    twitter_clean=twitter_clean.replace("RT ", "")
    

    #print(twitter_clean)
    ##Limpeza da string
    teste.append(twitter_clean)
    #print("-----------Predição---------",class_modelo.Models.predict(tweets,classes,teste))
    #results=[]
    #results.append(class_modelo.Models.predict(tweets,classes,teste))
    #with open('tweets.txt', 'a') as tf:
        #tf.write(class_modelo.Models.predict(tweets,classes,teste)[0])
    #print(class_modelo.Models.predict(tweets,classes,teste))
    
    text = twitter_clean
    socketio.emit('stream_channel',{'data': text, 'sentimento':class_modelo.Models.predict(tweets,classes,teste) },namespace='/demo_streaming')
    return True
 
  def on_error(self, status_code):
      print("Erro com o código:", status_code)
      return True # Não mata o coletor
 
  def on_timeout(self):
      print("Tempo esgotado!")
      return True # Não mata o coletor
  
  
    
class init_analysis(): 
            
        def init():
            
      #Criando o coletor com timeout de 60 seg
          streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener())
          streaming_api.filter(follow=None, track=consulta, languages=["pt"])



