#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:08:05 2022

@author: max
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


df = pd.read_csv("/Users/max/Downloads/EH_pbp_query_20212022_2022-04-25.csv")

#df.event_player_1.str.replace(".", " ", regex = False)

df["event_player_1"]=df["event_player_1"].str.replace('.',' ')
df["event_player_1"] = df["event_player_1"].str.title()

list_players = sorted(list(df.event_player_1.unique()))
list_dates = sorted(df.game_date.unique().tolist())

dic = {k:[] for k in list_players}

for i in list_dates:
    curr_date = df.loc[df.game_date == i]
    list_scorers = list(curr_date.event_player_1)
    for key in dic:
        if key not in list_scorers:
            dic[key].append(0)
        else:
            dic[key].append(list_scorers.count(key))
            

data = pd.DataFrame(dic)

cum = data.cumsum(axis = 0)

cum.index = list_dates

cum2 = cum.reset_index()
#%%

cole = cum2[["index", "Cole Caufield"]]
cole.columns = ["date", "goals"]

fig, ax = plt.subplots(figsize=(15,7))
plt.style.use('ggplot')
sns.lineplot(x=cole.date, y=cole['goals'], ax=ax)
ax.set_xticklabels(cole["date"])
#%%
def animate(i):
    data = cole.iloc[:int(i+1)] #select data range
    p = sns.lineplot(x=data.date, y=cole['goals'], ax=ax)
    p.tick_params(labelsize=17)
    plt.setp(p.lines,linewidth=7)
    
ani = FuncAnimation(fig, animate, frames=300, repeat=True)
ani.save('animation1.gif', writer='Pillow', fps=20)
#%%
cum2.index = cum2.index * 5

last_idx = cum2.index[-1] + 1
cum_expanded = cum2.reindex(range(last_idx))

cum_expanded['index'] = cum_expanded['index'].fillna(method='ffill')
cum_expanded = cum_expanded.set_index('index')

cum_rank_expanded = cum_expanded.rank(axis=1, method='first')
cum_expanded = cum_expanded.interpolate()

cum_rank_expanded = cum_rank_expanded.interpolate()
#%%
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

colors = ["#FFA7D1", "#E50000", "#E59500","#A06A42","#E5D900",
          "#94E044", "#02BE01", "#00D3DD","#0083C7","#0000EA",
          "#CF6EE4","#820080", "#FFA7D1", "#E50000", "#E59500",
          "#A06A42","#E5D900", "#94E044", "#02BE01", "#00D3DD",
          "#0083C7","#0000EA","#CF6EE4","#820080", "#FFA7D1",
          "#E50000", "#E59500","#A06A42","#E5D900","#94E044"]


def prepare_data(df, steps=5):
    df = df.reset_index()
    df.index = df.index * steps
    last_idx = df.index[-1] + 1
    df_expanded = df.reindex(range(last_idx))
    df_expanded['index'] = df_expanded['index'].fillna(method='ffill')
    df_expanded = df_expanded.set_index('index')
    df_rank_expanded = df_expanded.rank(axis=1, method='first')
    df_expanded = df_expanded.interpolate()
    df_rank_expanded = df_rank_expanded.interpolate()
    return df_expanded, df_rank_expanded

df_expanded, df_rank_expanded = prepare_data(cum)
df_expanded.head()

def init():
    ax.clear()
    nice_axes(ax)
    ax.set_ylim(0, 6.8)

def update(i):
    for bar in ax.containers:
        bar.remove()
    y = df_rank_expanded.iloc[i]
    width = df_expanded.iloc[i]
    ax.barh(y=y, width=width, color=colors, tick_label=labels)
    ax.tick_params(axis='y', labelsize= 12)
    date_str = str(df_expanded.index[i])
    ax.set_title(f'Habs leading goal scorers per day - {date_str}\n', fontfamily="DIN Condensed", fontsize=35)
    
fig = plt.Figure(figsize=(15, 13), dpi=200)
ax = fig.add_subplot()
anim = FuncAnimation(fig=fig, func=update, init_func=init, frames=len(df_expanded), 
                     interval=100, repeat=True)

anim.save('score.mp4')
#%%

