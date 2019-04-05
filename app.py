# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:16:55 2019

@author: Mirellebueno
"""
##Código de inicialização escrito com a ajuda do repositorio https://github.com/naushadzaman
#import gevent
from gevent import monkey

import os
import re
import json 
import time
import class_modelo
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
    
from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy 



async_mode = None

if async_mode is None:
    
   async_mode = 'gevent'
      
   print('async_mode is ' + async_mode)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, async_mode="threading",ping_timeout=30)
thread = None

## Keys Twitter API
consumer_key = 'TW9Jd0pnZll4NUrVGsKDu7hdc'
consumer_secret = 'YOlIsFvjioIZ4ZOe2VxHmnKmDOfed3rXvGktpseEeAdY6ScN0v'
access_token = '2666103462-34DtnGcugMlXiTe2eBfvKn3NcqtKtjtk4E0nwIk'
access_token_secret = '881rNts3uPn11xfNLDrach4gpC6INgsklY76KfIausmfM'


##Autentificação
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

print("Autentificão")
#Metodo responsavel por limpar o texto para o processamento
def clean_twitter(text): 
    twitter_clean=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    twitter_clean=twitter_clean.replace('RT', '')
    twitter_clean=twitter_clean.replace("..","")
    twitter_clean=twitter_clean.replace('"', "")
    twitter_clean=twitter_clean.replace("''", "")
    twitter_clean=twitter_clean.replace("p/", "")
    twitter_clean=twitter_clean.replace("RT ", "")
    return twitter_clean

def predict_twitter(twtter_test):
    
        classe_predita= class_modelo.Models.predict(twtter_test)[0];
        return classe_predita

class StdOutListener(StreamListener):
    def __init__(self):
        
        pass 
        
    def on_data(self, data):
        try: 
            
            time.sleep(5)
            
            tweet = json.loads(data)
            
            text = clean_twitter(tweet['text'])
          
            twitters=[]
            twitters.append(text)
            
            #sentimento=predict_twitter(train_dataset,twitter_train,target,twitters)
            sentimento=predict_twitter(twitters)
            
         
            
            #thread.sleep(5)
            print(text)
            print(sentimento)
            #Transmitindo...
            #socketio.sleep(5)
            socketio.emit('stream_channel',
                  {'data':tweet['text'], 'sentimento':sentimento,'imagem_thumb':tweet['user']['profile_image_url_https'],'objeto':tweet },
                  namespace='/demo_streaming')
           
            
        except: 
            pass 

    def on_error(self, status):
        print('Error status code', status)
        exit()


def background_thread():
    print("INICIALIZOU BACKEND")
    stream = Stream(auth, l)
    #_keywords = [':-)', ':-(']
    
    ##Apenas na Linguagem Portuguese
    stream.filter(follow=None, track='politica', languages=["pt"]) 
    


@app.route('/')
def index():
    
    
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
        
    return render_template('index.html')


l = StdOutListener()

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    server = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    #socketio.run(app, debug=True, host='127.0.0.1')
   #socketio.run(app, host="0.0.0.0", debug=True) # <host_ip_address> -- replace it with the IP address of your server where you are hosting 