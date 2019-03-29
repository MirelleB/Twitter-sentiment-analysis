# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 19:34:13 2019

@author: Mirellebueno
"""

from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return 'OK!'
if __name__=="__main__":
    app.run()