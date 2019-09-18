#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:36:01 2019

@author: stefancooper
"""

import pandas as pd
import statsmodels.datasets as sm
import os
from bs4 import BeautifulSoup
import requests
import matplotlib
from sklearn import preprocessing
import numpy as np
from sklearn import tree
from sklearn.tree import export_graphviz
import json
from pymongo import MongoClient

players = dict()

with open('config.json') as config_file:
    config_load = json.load(config_file)
mongo = config_load['mongoAddress']
client = MongoClient(mongo)
db = client.stefan
collection = db.custom_elo
collection.delete_many({ 'username': 'null' } )


client.close()