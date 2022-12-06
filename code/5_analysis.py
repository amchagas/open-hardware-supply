"""
preliminary analysis
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# paths
projectPath = Path()
while not (Path() / ".git").is_dir():
    projectPath = projectPath.parent
dataDir = projectPath / "data/derived3"
dataFile = dataDir / "upwData.json"
scoringFile = dataDir / "scoring_system.csv"

# data
documentData = pd.read_json(dataFile)
scoringData = pd.read_csv(scoringFile)
articles = documentData[documentData.genre.eq("journal-article")]

# plots
sns.jointplot(x=documentData.genre, y=documentData.oa_status)
sns.displot(documentData, x="oa_status", hue="genre")
sns.displot(articles, x="genre", hue="is_oa")

min_val = articles.year.min()
max_val = articles.year.max()
val_width = max_val - min_val
n_bins = max_val - min_val
bin_width = val_width / n_bins

sns.histplot(
    data=articles.year,
    bins=n_bins,
    binrange=(min_val, max_val),
    # x="year",
    # hue="day",
    # multiple = 'stack',
    # palette='Paired',
)
plt.xlim(2004, 2023)  # Define x-axis limits
plt.xticks(np.arange(min_val, max_val, 1), rotation=90)

sns.scatterplot(data=scoringData, x=range(22), y="total points ")
