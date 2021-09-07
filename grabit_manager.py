#-*-coding=utf-8-*-
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
import string
import os
import sys
import socket
import platform
#from dbhelper_SE import DBHelper

app = Flask(__name__)
#DB = DBHelper()


@app.route("/")
def index():
    return render_template("index.html")



if __name__=="__main__":
    app.run()




