#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

"""
Created on Sun Sep 15 12:12:08 2019

@author: stefancooper
"""

players = dict()

with open('config.json') as config_file:
    config_load = json.load(config_file)
mongo = config_load['mongoAddress']
client = MongoClient(mongo)
db = client.stefan
collection = db.custom_elo

# Collect player data from mongo
for player in collection.find():
    players[player.get('userId')] = [player.get('username'), player.get('ELO')]
# Update players with new information collected
print(players)
for pl in list(players):
    print(players.get(pl))
    myquery = { "userId": { "$regex": pl}}
    newvalues = { "$set": { "username": players.get(pl)[0], "ELO": 1000 } }
    x = collection.update_many(myquery, newvalues)
print("Players reset: ", len(players))

client.close()