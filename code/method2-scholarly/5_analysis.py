"""
Preliminary analysis
"""

import io
from functools import cache
import os
from pathlib import Path

import httpx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    dirs = get_directories()
    data_dir = dirs["data_dir"]
    out_dir = dirs["out_dir"]
    data = {**get_document_data(data_dir), **get_scoring_data(data_dir)}
    plot_doc(data["document"], out_dir)
    plot_art(data["article"], out_dir)
    plot_scoring(data["scoring"], out_dir)
    plot_joint_score_time(data["scoring"], out_dir)
    plot_joint_score_journal(data["scoring"], out_dir)


@cache
def _get_crossref_metadata(doi):
    return httpx.get(f"https://api.crossref.org/works/{doi}").json()


def _get_extracted_crossref_metadata(doi):
    data = _get_crossref_metadata(doi)
    return {
        "year": data["message"]["published"]["date-parts"][0][0],
        "journal": data["message"]["container-title"][0],
    }


def get_directories():
    print(f"\nCurrent directory is {os.getcwd()}")
    data_dir = Path(input("\nEnter path to the data directory: "))
    out_dir = Path(input("\nEnter path to the output directory: "))
    return {"data_dir": data_dir, "out_dir": out_dir}


def get_document_data(data_dir):
    combined_data_file_name = "wos_upwData_combined.json"
    document = pd.read_json(data_dir / combined_data_file_name)
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


def get_scoring_data():
    """
    Download a sheet from Google Spreadsheets (gds) by `key`.
    Return an enriched DataFrame.
    """
    gds_scoring_key = "1FqyM3ZwSqYrTSOx_0ddZzDjBz_c8wecN2xA_E-VyNsU"
    csv_text = _get_gds_export(
        document_key=gds_scoring_key, sheet_name="review1", export_format="csv"
    )
    scoring = pd.read_csv(io.StringIO(csv_text))
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
    fig.ax.set_xticks(range(article.year.min(), article.year.max() + 1))
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
