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

matches = list()
players = dict()
        
def scrapepopflash(user):
    response = requests.get("https://popflash.site/user/"+user)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    team1win = False
    team2win = False
    global players
    global matches
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
                        if nhyperlink.get('href')[-6:] not in players:
                            players[nhyperlink.get('href')[-6:]] = 1000
                        team1.append(nhyperlink.get('href')[-6:])
                    else:
                        team2.append(nhyperlink.get('href')[-6:])
                    playersCount+= 1

            for player, elo in players.items():
                if (player in team1 and team1win == True):
                    players[player] = elo +3
                    elo = elo + 50
                elif (player in team1 and team1win == False):
                    players[player] = elo -5
                    elo = elo - 100
                elif (player in team2 and team2win == True):
                    players[player] = elo +3
                    elo = elo + 50
                elif (player in team2 and team2win == False):
                    players[player] = elo -5
                    elo = elo - 100
def main():
    success = scrapepopflash("590843")
    if success == False:
        print("Too many requests, try again later")
    else:
        print("working...")
        for pl in list(players):
            success = ext_scrapepopflash(pl)
            if success == False:
                print("Too many requests, try again later")
                break
        print("Matches added: ",len(matches))
        print(matches)
        print(players)
        
def getUsername(data):
    start = data.find('<h3 style="text-transform: uppercase;"><span>', 0, 1000000)
    print(data[start+45:start+61])

main()
    
    
    
    
    
    
    
    