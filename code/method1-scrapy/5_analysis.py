"""
preliminary analysis
"""

from functools import cache
from pathlib import Path

import httpx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


@cache
def _get_crossref_metadata(doi):
    return httpx.get(f"https://api.crossref.org/works/{doi}").json()


def get_crossref_metadata(doi):
    data = _get_crossref_metadata(doi)
    return {
        "year": data["message"]["published"]["date-parts"][0][0],
        "journal": data["message"]["container-title"][0],
    }


#########
# Paths #
#########

projectPath = Path()
while not (Path() / ".git").is_dir():
    projectPath = projectPath.parent
dataDir = projectPath / "data/method1-scrapy-data/derived/20230214/"
dataFile = dataDir / "upwData.json"
scoringFile = dataDir / "May_2023_scoring system.csv"
figDir = projectPath / "figures"

########
# Data #
########

documentData = pd.read_json(dataFile)
documentData["year"] = documentData["year"].astype("Int64")
# articleData = documentData[documentData.genre.isin({"journal-article", "proceedings-article"})]
articleData = documentData[documentData.genre.isin({"journal-article"})]
scoringData = pd.read_csv(scoringFile)
scoringData = scoringData.dropna(subset=["total points "])
scoringData["_total_points"] = scoringData["total points "].mul(2).astype(int)
scoringData["_year"] = scoringData["paper DOI"].map(
    lambda x: get_crossref_metadata(x)["year"]
)
scoringData["_journal"] = (
    scoringData["paper DOI"]
    .map(lambda x: get_crossref_metadata(x)["journal"])
    .replace(
        {
            "PLoS ONE": "PLOS ONE",
            "American Journal of Physiology-"
            "Heart and Circulatory Physiology": "American Journal of Physiology",
        }
    )
)

#########
# Plots #
#########

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
fig.set_axis_labels("Genre")
fig.legend.set_title("Access")
fig.savefig(figDir / "documents-dist-genre_X_oa_status.png", dpi=300)

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
fig.set_axis_labels("Year")
fig.legend.set_title("Open Access")
fig.savefig(figDir / "articles-dist-year_X_is_oa.png", dpi=300)

plt.close()
fig = sns.displot(
    data=scoringData,
    x="_total_points",
    bins=range(0, 19),
    discrete=True,
    shrink=0.8,
    aspect=16 / 9,
    hue="_total_points",
    hue_norm=(0, 18 * 4 / 3),  # use colormap up to bright "open-style" oranges
    palette="PuOr_r",
)
fig.ax.set_xticks(range(0, 19))
fig.ax.set_yticks(range(0, scoringData["_total_points"].value_counts().max() + 1))
fig.legend.set_title("Score")
fig.set_axis_labels("Score")
fig.figure.savefig(figDir / "scoring-hist-_total_points.png", dpi=300)

plt.close()
fig = sns.jointplot(
    data=scoringData,
    x="_year",
    y="_total_points",
    kind="hist",
    joint_kws={"discrete": True},
    marginal_kws={"discrete": True},
)
fig.ax_joint.set_xticks(
    range(scoringData["_year"].min(), scoringData["_year"].max() + 1)
)
fig.ax_joint.set_yticks(range(0, 19))
fig.ax_joint.tick_params(rotation=45)
fig.set_axis_labels("Year", "Score")
fig.savefig(figDir / "scoring-joint-_total_points_X__year.png", dpi=300)


plt.close()
fig = sns.JointGrid(
    data=scoringData,
    x="_total_points",
    y="_journal",
    hue="_year",
)
fig.plot_joint(
    sns.swarmplot,
    size=7,
    order=sorted(scoringData["_journal"].unique()),
)
fig.plot_marginals(
    sns.histplot,
    multiple="stack",
    discrete=True,
)
fig.ax_joint.set_xticks(range(0, 19))
fig.set_axis_labels("Score", "Journal")
fig.ax_joint.legend().set_title("Year")
fig.savefig(figDir / "scoring-jointswarm-_total_points_X__journal_X__year.png", dpi=300)
