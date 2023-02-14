"""
preliminary analysis
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# paths
projectPath = Path()
while not (Path() / ".git").is_dir():
    projectPath = projectPath.parent
dataDir = projectPath / "data/derived/20230214/"
dataFile = dataDir / "upwData.json"
scoringFile = dataDir / "scoring_system.csv"
figDir = projectPath / "figures"

# data
documentData = pd.read_json(dataFile)
scoringData = pd.read_csv(scoringFile)
articleData = documentData[documentData.genre.eq("journal-article")]

# plots
plt.close()
fig = sns.jointplot(kind="hist", x=documentData.genre, y=documentData.oa_status)
fig.ax_joint.tick_params(rotation=30)
fig.savefig(figDir / "articles-joint-genre_X_oa_status.png")

plt.close()
fig = sns.displot(
    documentData,
    x="genre",
    hue="oa_status",
    hue_order=("gold", "green", "bronze", "hybrid", "closed"),
    multiple="dodge",
    shrink=0.8,
    aspect=16 / 9,
)
fig.savefig(figDir / "documents-dist-genre_X_oa_status.png")

plt.close()
fig = sns.displot(
    data=articleData,
    x="year",
    discrete=True,
    hue="is_oa",
    multiple="dodge",
    shrink=0.8,
    aspect=16 / 9,
)
fig.ax.set_xticks(range(articleData.year.min(), articleData.year.max() + 1))
fig.tick_params(rotation=45)
fig.savefig(figDir / "articles-dist-year_X_is_oa.png")

plt.close()
scoringData["total points"] = (2 * scoringData["total points "]).astype(int)
fig = sns.displot(
    data=scoringData,
    x="total points",
    bins=range(0, 22),
    discrete=True,
    shrink=0.8,
    aspect=16 / 9,
    hue="total points",
    hue_norm=(0, 20 * 4 / 3),  # use colormap up to bright "open-style" oranges
    palette="PuOr_r",
)
fig.ax.set_xticks(range(0, 21))
fig.ax.set_yticks(range(0, scoringData["total points"].value_counts().max() + 1))
fig.figure.savefig(figDir / "scoring-hist-total points .png")
