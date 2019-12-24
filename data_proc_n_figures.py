#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 15:18:32 2019

@author: andre
"""

#import sqlite3 as sq
#import csv
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
databaseLoc = "/home/andre/repositories/own/OSH_papers_DB/"
#databaseName = "zotero.sqlite"
csvName = "hardware.csv"
os.chdir(databaseLoc)

#db = sq.connect(databaseName)

fid = pd.read_csv(databaseLoc+csvName)

## clean up csv table
remove = ["Key","Call Number","Notes", "File Attachments",
          "Link Attachments","Series Editor",
          "Translator","	Contributor","Attorney Agent","Book Author",
          "Cast Member","Commenter""Composer","Cosponsor","Counsel",
          "Interviewer","Producer","Recipient","Reviewed Author",
          "Scriptwriter","Words By","Guest","Number","Edition",
          "Running Time","Scale	Medium","Artwork Size","Filing Date",
          "Application Number","	Assignee","Issuing Authority	","Country",
          "Meeting Name", "Conference Name","Court","References"	,"Reporter",
          "Legal Status","Priority Numbers""Programming Language","Version", 
          "System","Code","Code Number","Section","Session","Committee",
          "History","Legislative Body"
          ]

#remove link to file attachments (as they just contain paths to my local files)
for item in remove:
    if item in fid.keys():
        fid.pop(item)


#index of publications (the dataset also has webpages, conference papers, etc)
pubIndex = fid[fid["Item Type"]=="journalArticle"].index

#generate another pandas dataframe with only publications
onlyPubs = fid.loc[pubIndex]


#publication year histogram
#pubYear = pd.DataFrame(data=fid['Publication Year'].values,columns=["year"],dtype=int)

#rearrange data to be sorted by publication year
fid = fid.sort_values("Publication Year")
label1 = fid["Publication Year"]
label1 = label1.dropna()
label1 = label1.astype("int64")
label1 = label1.unique()

fig1 = sns.catplot(x="Publication Year", kind="count",  data=fid,color="r")
fig1.set_xticklabels(label1)

#set aside only journal articles
pubIndex = fid[fid["Item Type"]=="journalArticle"].index
onlyPub = fid.loc[pubIndex]
onlyPub = onlyPub.sort_values("Publication Title")




fig2 = sns.catplot(x="Publication Title", kind="count", data=onlyPub,color="r");
fig2.set_xticklabels(rotation=90)

fig2.savefig("/home/andre/Desktop/test.png")



#only preprints

#fid.columns.tolist()

#columns = fid.columns.tolist()
#source =  ColumnDataSource(fid["Publication Year"])
#journals = source.data['Publication Title'].tolist()

#number of publications fby year
#fid["Publication Year"].hist(bins=range(2007,2021))
#sns.distplot(fid["Publication Title"].dropna(),bins=range(2007,2021),
#             kde=False,axlabel="year",
#             vertical=False, norm_hist=False)

#fid["Publication Title"].dropna().hist()
