#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:24:30 2019

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
import operator


players = dict()

with open('config.json') as config_file:
    config_load = json.load(config_file)
mongo = config_load['mongoAddress']
client = MongoClient(mongo)
db = client.stefan
collection = db.custom_elo

# Collect player data from mongo
for player in collection.find():
    players[player.get('username')] = player.get('ELO')
# Update players with new information collected
sort= sorted(players.items(), key=operator.itemgetter(1), reverse = True)
leaderboard = ""
playersString=""
scoresString=""
for pl in sort:
    if isinstance(pl[0], str) and isinstance(pl[1], int) and pl[0] != "null":
        leaderboard = leaderboard + "" + pl[0] + ": **" +str(pl[1]) + "** | "
        playersString = playersString + pl[0] + "!@£%&"
        scoresString = scoresString + str(pl[1]) + "!@£%&"
'''discordmess = {embed: {
      color: 3447003,
      title: "Test:",
      fields: [
        { name: "Players", value: "'''+playersString+'''", inline: true},
        { name: "Scores", value: "'''+scoresString+'''", inline: true}
      ]
    }'''
print(playersString)
print(scoresString)

client.close()