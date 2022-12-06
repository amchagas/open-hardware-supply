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
dataDir = projectPath / "data/derived3"
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
fig = sns.displot(documentData, x="oa_status", hue="genre")
fig.savefig(figDir / "documents-dist-oa_status_X_genre.png")

plt.close()
fig = sns.displot(articleData, x="genre", hue="is_oa")
fig.savefig(figDir / "articles-dist-genre_X_is_oa.png")

plt.close()
fig = sns.histplot(
    data=articleData.year,
    discrete=True,
)
fig.set_xticks(range(articleData.year.min(), articleData.year.max() + 1))
fig.tick_params(rotation=30)
fig.figure.tight_layout()
fig.figure.savefig(figDir / "articles-hist_year.png")

plt.close()
totalPoints = (2 * scoringData["total points "]).astype(int)
fig = sns.histplot(data=totalPoints, bins=range(0, 22), discrete=True)
fig.set_xticks(range(0, 21))
fig.figure.savefig(figDir / "scoring-hist-total points .png")
