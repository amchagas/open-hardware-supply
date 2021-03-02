#! /bin/env python3

from pathlib import Path
import pandas as pd

# Project folder structure

baseDir = Path("..")
dataSourceDir = baseDir / 'data' / 'sources'
dataOutDir = baseDir / 'data' / 'derived'
figDir = baseDir / 'figures'

# Project files shared across notebooks

allDataFile = dataOutDir / 'all_data.json.xz'
articleDataFile = dataOutDir / 'article_data.json.xz'

# Project-wide functions

def store_data(dataFrame, dataFile):
    dataFrame.to_json(dataFile, orient='table')


def load_data(dataFile):
    return pd.read_json(dataFile, orient="table", convert_dates=False)


def build_query():
    nouns = [
        'equipment',
        'hardware',
        'labware',
    ]
    adjectives = [
        'open',
        'open source',
        'open science',
        'frugal',
        #'low cost',
    ]
    phrases = [
        ' '.join([a, n]) for a in adjectives for n in nouns
    ]
    phrases.extend([
        "free hardware and software",
    ])
    query = " OR ".join(f'"{x}"' for x in phrases)

    return query
