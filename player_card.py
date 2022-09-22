#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 22:57:21 2022

@author: max
"""

import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec 
import matplotlib.patheffects as path_effects
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from mplsoccer.pitch import Pitch
from hockey_rink import NHLRink

import pandas as pd
import numpy as np

from PIL import Image
import requests
from io import BytesIO

from highlight_text import HighlightText, ax_text, fig_text
from datetime import date, datetime

#%%
cat = ["EV Offense", "EV Defense", "PP", "PK", "Finishing",
       "G/60", "A/60", "Penalties", "Competition", "Teammates"]
numba = list(np.random.randint(low = 0,high=99,size=10))

df = pd.DataFrame()
df["cat"] = cat
df["numba"] = numba

player, num, pos = "Cole Caufield", "#22", "RIGHT WINGER"

#df = pd.DataFrame(np.random.randint(0,100,size=(200, 2)), columns=['X', 'Y'])
fig = plt.figure(figsize=(10,10), dpi = 140)
grid = plt.GridSpec(6, 6)

a1 = fig.add_subplot(grid[1:6, 0:3])
a2 = fig.add_subplot(grid[0:1, 1:5],sharex=a1)
a3 = fig.add_subplot(grid[0:1, 0:1])
a4 = fig.add_subplot(grid[1:3, 3:5])
a5 = fig.add_subplot(grid[4:6, 3:5], sharex=a4)

#a3 = fig.add_subplot(grid[0:5, 5],sharey=a1)

a1.barh(cat, numba, align='center', zorder = 5)
ypos = np.arange(len(cat))
a1.grid(ls="dotted",lw="0.5",color="grey", zorder=1)
bars = a1.barh(range(len(cat)), numba, color = "darkblue", zorder=5)

a1.bar_label(bars, padding = 5, )


#a1.set_yticklabels(cat, minor=False)
#a1.set_yticks(y_pos)
a1.invert_yaxis()  # labels read top-to-bottom
a1.set_xlabel('Percentile')
a1.set_title('Individual Statistics')

a1.spines["right"].set_visible(False)
a1.spines["top"].set_visible(False)
a1.spines["left"].set_visible(False)
a1.spines["bottom"].set_visible(False)

a1.set_xlim(0,100)

rink = NHLRink(rotation=90)
a4 = rink.draw(ax=a4, display_range = "offense")
a4.set_title('Offense', fontfamily="DIN Condensed", color = "purple",fontsize=20)
a4.scatter(list(np.random.randint(low = -42.5,high=42.5,size=100)), list(np.random.randint(low = 0,high=100,size=100)), s = 10, color = "purple")
#a4.hexbin(list(np.random.randint(low = -42.5,high=42.5,size=100)), list(np.random.randint(low = 0,high=100,size=100)), gridsize = 15, cmap = "Reds")

a5 = rink.draw(ax=a5, display_range = "defense")
a5.set_title('Defense', fontfamily="DIN Condensed", color = "green", fontsize=20)
a5.scatter(list(np.random.randint(low = -42.5,high=42.5,size=100)), list(np.random.randint(low = -100,high=0,size=100)), s = 10, color = "green")

a2.axis("off")
a2.text(10,0.5, f"{player}, {num}",fontsize=40, fontfamily="DIN Condensed", color = "darkblue")
a2.text(10,0.1, f"{pos}",fontfamily="DIN Condensed",fontsize=25, color = "darkblue")


a3.axis("off")
path = "/Users/max/Documents/My Tableau Repository/Shapes/NHL logos/MON.svg.png"
img = Image.open(path)
a3.imshow(img)

# =============================================================================
# pitch = Pitch(pitch_type='opta', orientation='vertical', stripe=False)
# pitch.draw(ax=a1)
# pitch.scatter(df['X'], df['Y'],
#                     s=10, c='black', label='scatter', ax=a1)
# =============================================================================

#a2.hist(df['Y'], 3, color = 'black', histtype='stepfilled')
#a3.hist(df['X'], 9, orientation='horizontal', color='black', histtype='stepfilled')

plt.show()