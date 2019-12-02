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
databaseLoc = "/home/andre/repositories/own/OSH_papers_DB/"
#databaseName = "zotero.sqlite"
csvName = "hardware.csv"
os.chdir(databaseLoc)

#db = sq.connect(databaseName)

fid = pd.read_csv(databaseLoc+csvName)

## clean up csv table
remove = ["Key","Call Number","Extra","Notes", "File Attachments",
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

#publication year histogram
pubYear = fid['Publication Year']

sns.distplot(pubYear.dropna(),
             rug=False,kde=False,
             bins=range(2007,2021))


#journal and preprint histogram
allPub = fid["Publication Title"]
allPub.hist()

#only preprints




