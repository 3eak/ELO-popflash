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
from pymongo import MongoClient
from pprint import pprint
import json

with open('config.json') as config_file:
    config_load = json.load(config_file)


matches = list()
players = dict()
        
mongo = config_load['mongoAddress']
client = MongoClient(mongo)
db = client.stefan
collection = db.custom_elo
collection_matches = db.matches

def scrapepopflash(user, name):
    response = requests.get("https://popflash.site/user/"+user)
    data = response.text
    
    soup = BeautifulSoup(data, 'html.parser')
    team1win = False
    team2win = False
    global players
    global matches
    for player, elo in players.items():
        if player == user:
            players[player] = [getUsername(data), elo[1]]

    if "Too many requests" in data:
        return False

    for hyperlink in soup.find_all('a'):
        if ("/match/" in hyperlink.get('href') and hyperlink.get('href') not in matches):
            matches.append(hyperlink.get('href'))
            match = requests.get("https://popflash.site"+hyperlink.get('href'))
            nsoup = BeautifulSoup(match.text, 'html.parser')
            t1win = """      <div class="score score-1">
        16
      </div>"""
            if  t1win in  match.text:
                team1win = True
                team2win = False
            else:
                team2win = True
                team1win = False
            playersCount = 0
            team1 = list()
            team2 = list()
            for nhyperlink in nsoup.find_all('a'):
                if "/user/" in nhyperlink.get('href'):
                    if playersCount < 5:
                        ''' Used for adding new players
                        if nhyperlink.get('href')[6:] not in players:
                            players[nhyperlink.get('href')[6:]] = ["null", 1000]
                            collection.insert_one({"userId": nhyperlink.get('href')[6:], "username": "null", "ELO": 1000})
                        '''
                        team1.append(nhyperlink.get('href')[6:])
                    else:
                        team2.append(nhyperlink.get('href')[6:])
                    playersCount+= 1

            for player, elo in players.items():
                if (player in team1 and team1win == True):
                    players[player] = [elo[0], elo[1] + 3]
                elif (player in team1 and team1win == False):
                    players[player] = [elo[0], elo[1] - 5]
                elif (player in team2 and team2win == True):
                    players[player] = [elo[0], elo[1] + 3]
                elif (player in team2 and team2win == False):
                    players[player] = [elo[0], elo[1] - 5]
def main():

    # Collect matches from mongo
    for match in collection_matches.find():
        matches.append(match.get('matchId'))
    oldMatches = len(matches)
    # Collect player data from mongo
    for player in collection.find():
        players[player.get('userId')] = [player.get('username'), player.get('ELO')]
    # Loop through each player and recursively get each match played
    #print(players)
    for player in collection.find():
        #print(player.get('userId'))
        success = scrapepopflash(player.get('userId'), player.get('username'))
        if success == False:
            print("Too many requests, try again later")
            break
    # Update players with new information collected
    for pl in list(players):
        myquery = { "userId": { "$regex": pl}}
        newvalues = { "$set": { "username": players.get(pl)[0], "ELO": players.get(pl)[1] } }
        collection.update_many(myquery, newvalues)
    for i in range(len(matches)):
        collection_matches.insert_one({"matchId": matches[i]})

    client.close()
    print("Matches added: ",len(matches)-oldMatches)
        
def getUsername(data):
    start = data.find('<h3 style="text-transform: uppercase;"><span>', 0, 1000000)
    return data[start+45:data.find('<',start+45, 1000000)]

main()
    
    
    
    
    
    
    
    