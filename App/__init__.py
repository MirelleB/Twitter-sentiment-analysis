# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 21:31:28 2019

@author: Mirellebueno
"""


from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World! FUNCIONOU CARAI THE WINTER IS COMMING"

if __name__ == "__main__":
    app.run(debug=True)