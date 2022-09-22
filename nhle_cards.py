#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:41:59 2022

@author: max
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import urllib.request

nhle = pd.read_csv("/Users/max/romanov.csv")
nhle = nhle.iloc[: , 1:]
nhle = df = pd.concat([nhle, pd.DataFrame.from_records([{ 'League' : 'nhl', 'NHLe' : 1 }])])

link = "https://www.eliteprospects.com/player/527430/filip-mesar"
team_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Montreal_Canadiens.svg/2560px-Montreal_Canadiens.svg.png"
player_name = "Filip Mešár"
#team_3 = "CAR"
color_1 = "blue"
color_2 = "darkblue"
title = "MEŠÁR IS COMING TO NORTH AMERICA"
bb_distance = 1.5
urllib.request.urlretrieve(team_logo,"logo.png")
  

def nhle_graph():
    player_df = pd.read_html(link)[1]
    #player_df = player_df.iloc[:-1]   
    player_df["league_min"] = player_df["League"].str.lower()
    
    leagues_nhle = set(nhle.League) #Lists are too heavy, so sets do the work
    keep = [] #indexes to keep
    for i in range(len(player_df)):
        if player_df.league_min[i] in leagues_nhle:
            keep.append(i)
    
         
    player_df = player_df.iloc[keep].reset_index(drop=True)
    player_df[["GP", "TP"]] = player_df[["GP", "TP"]].apply(pd.to_numeric)
    
    val = []
    dic = dict(zip(nhle.League, nhle.NHLe))
    
    for i in range(len(player_df)):
        val.append((player_df.TP[i])*(dic[player_df.league_min[i]]))
        
    player_df["nhle"] = val
    
    szns_leagues = []
    
    for season in player_df.S.unique().tolist():
        season_df = player_df[player_df.S == season].reset_index(drop=True)
        leagues = season_df.League.unique().tolist()
        leagues_str = '/'.join(str(league) for league in leagues)
        szns_leagues.append(leagues_str)
        
    global sun
    
    sun = player_df.groupby(["S"], as_index=False)[["GP", 'nhle']].sum()
    sun["82_nhle"] = 82*(sun["nhle"]/sun["GP"])
    sun["League"] = szns_leagues
    
    #sun = sun.iloc[len(sun)-5:]
    
    
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    seasons_list = sun.S.tolist()
    nhle_82 = sun["82_nhle"].tolist()
    leagues = sun.League.tolist()
    
    ax.scatter(seasons_list,nhle_82, s=60, color = f"{color_1}")
    ax.plot(seasons_list, nhle_82, color = f"{color_1}", zorder = 1)
    #plt.axvline(x=2, color = "r", ls= "--")
    #ax.text(2.1, 53, "*Draft year", color="r")
    
    title_font, body_font = "DIN Condensed","DIN Condensed"
    text_color = f"{color_2}"
    
    fig.text(0.27,0.94, f"\n{title}\n", fontweight="bold",fontsize=30, fontfamily=title_font,color=text_color)
    
    fig.text(0.27,.94,F"Look at {player_name}'s NHLe since his career began",fontweight="regular", style ="italic", fontsize=20,fontfamily=body_font, color=text_color)
    
    #fig.text(0.27,.94,F"Look at {player_name}'s NHLe in the last 5 seasons",fontweight="regular", style ="italic", fontsize=20,fontfamily=body_font, color=text_color)

    ax2 = fig.add_axes([0.1,0.95,0.15,0.15]) # badge
    ax2.axis("off")
    #ax2.imshow(Image.open(f"/Users/max/Documents/My Tableau Repository/Shapes/NHL logos/{team_3}.svg.png"))
    ax2.imshow(Image.open("logo.png"))
    
    fig.text(0.9, -0.025, f"Viz and model by the homie @woumaxx", horizontalalignment = "right",
            fontstyle="italic",fontsize=9, color=text_color)
    
    
    for i in range(len(sun)):
        y = nhle_82[i]
        text = leagues[i]
        if i in [2,6,7,8,9] :
            ax.text(i,y-bb_distance,text, horizontalalignment='center', color='black', bbox=dict(facecolor='w', edgecolor='black', boxstyle='round,pad=.6'))
        else:
            ax.text(i,y+bb_distance-1,text, horizontalalignment='center', color='black', bbox=dict(facecolor='w', edgecolor='black', boxstyle='round,pad=.6'))
    
    #ax.set_xticklabels(seasons_list)
    ax.tick_params(axis='x', labelrotation= 0)
    # Show graphic
    #plt.style.use('ggplot')
    plt.savefig('pel.png', bbox_inches = "tight", dpi = 500)
    return plt.show()


nhle_graph()    
    