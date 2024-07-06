from flask import Flask, request
from os.path import isfile, join
from mimetypes import MimeTypes
from os import listdir
import hashlib
import json
import hmac
import copy
import sys
import os



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getTags", methods = ["POST"])
def getTags():
