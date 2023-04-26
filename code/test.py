#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:50:17 2023

@author: andre
"""

import pandas as pd
import json

import os

os.getcwd()
sample = "../data/open hardware - 2005"

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