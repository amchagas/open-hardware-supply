"""
preliminary analysis
"""
import matplotlib.pyplot as plt
import numpy as np
#import requests
import pandas as pd
import seaborn as sns
#from pyzotero import zotero
#import json
#import time


dataPath = "../data/derived3/"
dataFile = "upwData.json"
data = pd.read_json(dataPath + dataFile)

data2 = pd.read_csv(dataPath+"scoring_system.csv")
articles = data[data.genre=="journal-article"]
#idx = set(articles.doi)


sns.jointplot(data.genre,data.oa_status)
sns.displot(data, x="oa_status", hue="genre")
sns.displot(articles, x="genre", hue="is_oa")


min_val = articles.year.min()
max_val = articles.year.max()
val_width = max_val - min_val
n_bins = max_val-min_val
bin_width = val_width/n_bins

sns.histplot(#x="year",
                #hue="day", multiple = 'stack', 
                data=articles.year,
                bins=n_bins, binrange=(min_val, max_val),
                )
                #palette='Paired')
plt.xlim(2004, 2023) # Define x-axis limits
plt.xticks(np.arange(min_val, max_val, 1),rotation=90)

sns.scatterplot(data=data2, x=range(22), y="total points ")
