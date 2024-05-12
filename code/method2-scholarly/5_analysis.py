"""
Preliminary analysis
"""

from functools import cache
import logging
import os
from pathlib import Path
import readline

import httpx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)

# Restrict delims so completion works with paths.
readline.set_completer_delims("\t\n")
readline.parse_and_bind("tab: complete")

PATHS = {"data_dir": None,
         "data_path": None,
         "out_dir": None}

#/home/andre/repositories/open-hardware-supply/data/raw/method2-scholarly-data
#/home/andre/repositories/open-hardware-supply/data/raw/method2-scholarly-data/open_hardwarewos_upwData_combined.json
#/home/andre/repositories/open-hardware-supply/data/raw/method2-scholarly-data/output



def main():
    setup_paths()
    data_dir = PATHS["data_dir"]
    out_dir = PATHS["out_dir"]
    data_path = PATHS["data_path"]
    data = {**get_document_data(data_path), **get_scoring_data(data_dir)}
    plot_doc(data["document"], out_dir)
    plot_art(data["article"], out_dir)
    plot_scoring(data["scoring"], out_dir)
    plot_joint_score_time(data["scoring"], out_dir)
    plot_joint_score_journal(data["scoring"], out_dir)


if "_get_crossref_metadata" not in globals():
    """So as to not restart the cache when reloading."""

    @cache
    def _get_crossref_metadata(doi):
        return httpx.get(f"https://api.crossref.org/works/{doi}").json()


def _get_extracted_crossref_metadata(doi):
    data = _get_crossref_metadata(doi)
    return {
        "year": data["message"]["published"]["date-parts"][0][0],
        "journal": data["message"]["container-title"][0],
    }


def setup_paths():
    print(f"\nCurrent directory is {os.getcwd()}")
    if PATHS["data_dir"] is None:
        PATHS["data_dir"] = Path(input("Enter path to the data directory: ").strip())
    if PATHS["data_path"] is None:
        PATHS["data_path"] = Path(input("Enter path to the data file: ").strip())
    if PATHS["out_dir"] is None:
        PATHS["out_dir"] = Path(input("Enter path to the output directory: ").strip())
    PATHS["out_dir"].mkdir(exist_ok=True)


def get_document_data(data_path):
    document = pd.read_json(data_path)
    article = document[document.genre.eq("journal-article")]
    return {"document": document, "article": article}


def _get_gds_export(document_key, sheet_name, export_format="csv"):
    gds_base_tpl = "https://docs.google.com/spreadsheets/d/{document_key}"
    gds_export_tpl = (
        gds_base_tpl + "/gviz/tq?tqx=out:{export_format}&sheet={sheet_name}"
    )
    gds_export_url = gds_export_tpl.format(
        document_key=document_key, sheet_name=sheet_name, export_format=export_format
    )
    return httpx.get(gds_export_url).text


def get_scoring_data(data_dir):
    """
    Download a sheet from Google Spreadsheets (gds) by `key` and return an enriched
    DataFrame.
    """
    score_path = Path(data_dir / "score_cache.csv")
    try:
        gds_scoring_key = "1FqyM3ZwSqYrTSOx_0ddZzDjBz_c8wecN2xA_E-VyNsU"
        csv_text = _get_gds_export(
            document_key=gds_scoring_key, sheet_name="review1", export_format="csv"
        )
        score_path.write_text(csv_text)
    except Exception:
        logger.warning("Downloading score sheet failed, will try cached version.")
    scoring = pd.read_csv(score_path)
    scoring["_total_points"] = scoring["total points "].mul(2).astype("Int64")
    scoring["_year"] = scoring["paper DOI"].map(
        lambda x: _get_extracted_crossref_metadata(x)["year"]
    )
    scoring["_journal"] = (
        scoring["paper DOI"]
        .map(lambda x: _get_extracted_crossref_metadata(x)["journal"])
        .replace(
            {
                "PLoS ONE": "PLOS ONE",
                "American Journal of Physiology-"
                "Heart and Circulatory Physiology": "American Journal of Physiology",
            }
        )
    )
    return {"scoring": scoring}


def plot_doc(document, out_dir):
    plt.close()
    fig = sns.displot(
        document,
        x="genre",
        hue="oa_status",
        hue_order=("gold", "green", "bronze", "hybrid", "closed"),
        multiple="dodge",
        shrink=0.8,
        aspect=16 / 9,
    )
    fig.set_axis_labels("Genre")
    fig.legend.set_title("Access")
    fig.savefig(out_dir / "documents-dist-genre_X_oa_status.png", dpi=300)


def plot_art(article, out_dir):
    plt.close()
    fig = sns.displot(
        data=article,
        x="year",
        discrete=True,
        hue="is_oa",
        multiple="dodge",
        shrink=0.8,
        aspect=16 / 9,
    )
    fig.ax.set_xticks(range(int(article.year.min()), int(article.year.max()) + 1))
    fig.tick_params(rotation=45)
    fig.set_axis_labels("Year")
    fig.legend.set_title("Open Access")
    fig.savefig(out_dir / "articles-dist-year_X_is_oa.png", dpi=300)


def plot_scoring(scoring, out_dir):
    plt.close()
    fig = sns.displot(
        data=scoring,
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
    fig.ax.set_yticks(range(0, scoring["_total_points"].value_counts().max() + 1))
    fig.legend.set_title("Score")
    fig.set_axis_labels("Score")
    fig.figure.savefig(out_dir / "scoring-hist-_total_points.png", dpi=300)


def plot_joint_score_time(scoring, out_dir):
    plt.close()
    fig = sns.jointplot(
        data=scoring,
        x="_year",
        y="_total_points",
        kind="hist",
        joint_kws={"discrete": True},
        marginal_kws={"discrete": True},
    )
    fig.ax_joint.set_xticks(range(scoring["_year"].min(), scoring["_year"].max() + 1))
    fig.ax_joint.set_yticks(range(0, 19))
    fig.ax_joint.tick_params(rotation=45)
    fig.set_axis_labels("Year", "Score")
    fig.savefig(out_dir / "scoring-joint-_total_points_X__year.png", dpi=300)


def plot_joint_score_journal(scoring, out_dir):
    plt.close()
    fig = sns.JointGrid(
        data=scoring,
        x="_total_points",
        y="_journal",
        hue="_year",
    )
    fig.plot_joint(
        sns.swarmplot,
        size=7,
        order=sorted(scoring["_journal"].unique()),
    )
    fig.plot_marginals(
        sns.histplot,
        multiple="stack",
        discrete=True,
    )
    fig.ax_joint.set_xticks(range(0, 19))
    fig.set_axis_labels("Score", "Journal")
    fig.ax_joint.legend().set_title("Year")
    fig.savefig(
        out_dir / "scoring-jointswarm-_total_points_X__journal_X__year.png", dpi=300
    )


if __name__ == "__main__":
    main()
