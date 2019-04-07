# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:16:55 2019

@author: Mirellebueno
"""


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
from json import dumps
from kafka import KafkaProducer,KafkaConsumer
from json import loads
    
    
from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy 
from queue import Queue


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, async_mode="threading",ping_timeout=30)
thread = None

## Keys Twitter API
consumer_key = 'TW9Jd0pnZll4NUrVGsKDu7hdc'
consumer_secret = 'YOlIsFvjioIZ4ZOe2VxHmnKmDOfed3rXvGktpseEeAdY6ScN0v'
access_token = '2666103462-34DtnGcugMlXiTe2eBfvKn3NcqtKtjtk4E0nwIk'
access_token_secret = '881rNts3uPn11xfNLDrach4gpC6INgsklY76KfIausmfM'


##Authentication API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

q = Queue()


# Kafka Configuration
producer = KafkaProducer(bootstrap_servers=['http://twitter-sentiment-analysi.herokuapp.com/'], value_serializer=lambda x: dumps(x).encode('utf-8'))
                        

#Method to clear the text
def clean_twitter(text): 
    twitter_clean=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    twitter_clean=twitter_clean.replace('RT', '')
    twitter_clean=twitter_clean.replace("..","")
    twitter_clean=twitter_clean.replace('"', "")
    twitter_clean=twitter_clean.replace("''", "")
    twitter_clean=twitter_clean.replace("p/", "")
    twitter_clean=twitter_clean.replace("RT ", "")
    return twitter_clean

#Method returns predicted class of new twitter 

def predict_twitter(twtter_test):
    
        predicted_class= class_modelo.Models.predict(twtter_test)[0];
        return predicted_class

#class Stream Listener
class TwitterListener(StreamListener):
    def __init__(self):
       
        pass 
        
    def on_data(self, data):
        try: 
           
            tweet = json.loads(data)
            producer.send('twitter_stream', tweet)
            #text_processing(tweet)
            #time.sleep(5)
        except: 
            pass 

    def on_error(self, status):
        print('Error status code', status)
        exit()
        

#Method to process and return result for socketio
def text_processing():
    
    consumer = KafkaConsumer('twitter_stream', bootstrap_servers=['http://twitter-sentiment-analysi.herokuapp.com/'], auto_offset_reset='earliest',enable_auto_commit=True,group_id='my-group',value_deserializer=lambda x: loads(x.decode('utf-8')))
    
    for get_tweet in consumer:
        text = clean_twitter(get_tweet['text'])
          
        twitters=[]
        twitters.append(text)
            
    
        sentiment=predict_twitter(twitters)
        socketio.emit('stream_channel',
                      {'data':get_tweet['text'], 'sentimento':sentiment,'imagem_thumb':get_tweet['user']['profile_image_url_https'],'objeto':get_tweet },
                      namespace='/demo_streaming')
        
            
   
    
def background_thread():
    stream = Stream(auth, l)
    stream.filter(follow=None, track='politica', languages=["pt"]) 
    


@app.route('/')
def index():
    
    
    global thread
    if thread is None:
          thread = Thread(target=background_thread)
          thread.daemon = True
          thread.start()
          text_processing()
           
    return render_template('index.html')


l = TwitterListener()

if __name__ == '__main__':
    server = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    