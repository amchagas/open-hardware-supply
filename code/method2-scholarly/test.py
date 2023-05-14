#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:50:17 2023

@author: andre
"""

import pandas as pd
import json
import re
import os
#from tqdm.auto import tqdm
import logging


os.getcwd()
sample = "../data/open hardware - 2005"
"""
# Read JSON data from file
with open(sample, 'r') as file:
    json_data = file.readlines()

# Remove newline characters and parse JSON
json_data = [json.loads(line.strip()) for line in json_data]

# Extract relevant data from JSON
extracted_data = []
for data in json_data:
    extracted_data.append({
        'title': data['bib'].get('title', None),
        'author': data['bib'].get('author', None),
        'first_author': data['bib'].get('author', None)[0],
        "pub_year": data['bib'].get('pub_year', None),
        #"first_author": data['bib'].get('first_author', None),
        'pub_type': data.get('container_type', None),
        'venue': data['bib'].get('venue', None),
        'pub_url': data.get('pub_url', None)
    })

# Convert extracted data to Pandas DataFrame
df = pd.DataFrame(extracted_data)
df.to_json("../data/test.json")

print(df)
"""
normalize_rex = re.compile(r"\W+")
def _logging():
    logger = logging.getLogger(f"{type(self).__module__}.{type(self).__name__}")
    logger.setLevel(logging.DEBUG)
    logFileName = time.asctime().replace(" ","_").replace(":","_")
    fh = logging.FileHandler(store / f"{logFileName}.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger
def normalize_text(text):
    return normalize_rex.sub(" ", text).strip().lower()



print("files found: "+str(len(source_paths)))
for idx,fpath in enumerate(source_paths):
    print("processing file "+str(idx))
    print(fpath)
    with open(fpath,'r') as f:
        json_data = f.readlines()
    # Remove newline characters and parse JSON
    json_data = [json.loads(line.strip()) for line in json_data]
    # Extract relevant data from JSON
    extracted_data = []
    for data in json_data:
        
        temp = {
            'title': data['bib'].get('title', None),
            'author': data['bib'].get('author', None),
            "pub_year": data['bib'].get('pub_year', None),
            #"first_author": data['bib'].get('first_author', None),
            'pub_type': data.get('container_type', None),
            'venue': data['bib'].get('venue', None),
            'pub_url': data.get('pub_url', None)
        }
        if temp['author']:
            temp['first_author']=temp['author'][0]
        else:
            temp['first_author']="NA"
        
        if pubyear := re.search(r"[,-] (\d{4}) -", temp["pub_year"]) == "NA":
            print("missing year")
            #logger.debug(("Missing year", temp))
            
        yield temp
        
    