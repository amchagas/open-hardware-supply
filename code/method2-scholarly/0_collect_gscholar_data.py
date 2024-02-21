import calendar
from contextlib import nullcontext
import json
import logging
from pathlib import Path

from scholarly import scholarly

#use free proxies, as Google Scholar is blocking access for these many entries
from scholarly import ProxyGenerator

with open("scraper_api_key") as fh:
    key = fh.readline()

pg = ProxyGenerator()
#success = pg.FreeProxies()
success = pg.ScraperAPI(key)

scholarly.use_proxy(pg)

if "logger" not in locals():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

# Keep it simple and close to the essential terms,
# and so in the scope of claiming OSH qualities
TERMS = (
#    "open hardware",
    "open source hardware",
#    "open science hardware",
#    "open scientific hardware",
#    "open source instrument",
#    "open source instrumentation",
#    "open labware"
)

# 2005 → Arduino, Make, Git, ...
# full_query [< 2005]: 615 results
# full_query [>=2000 & < 2005]: 335 results
YEARS = tuple(range(2017, 2018))


# Months in current locale (English with the default locale)
# We exclude month 5 (May), as it coincides with the verb "may".
MONTHS = tuple(calendar.month_name[m] for m in range(1, 13) if m != 5)

LANGUAGES = tuple("en")

# Query results are silently cut at 1k
QUERY_MAX_RESULTS = 1000


class QueryBuilder:
    @staticmethod
    def quote(x):
        return f'"{x}"'
    """
    @staticmethod
    #choose language articles are written in
    def lang(x):
        return f'"{x}"'
    """
    @staticmethod
    def or_(*xs):
        return "(" + " OR ".join(xs) + ")"

    @staticmethod
    def not_(x):
        """NOTs must go at the end and outside nontrivial parenthesis"""
        return f"-{x}"

    @staticmethod
    def and_(*xs):
        return "(" + " ".join(xs) + ")"


def get_full_query(terms):
    #return QueryBuilder.or_(QueryBuilder.quote(term) for term in terms)
    return QueryBuilder.or_(QueryBuilder.quote(terms))

def get_pubs(query, year_low=None, year_high=None, start_index=0, **kwargs):
    search_pubs_args = {"year_low": year_low, "year_high": year_high, **kwargs}
    pubs = scholarly.search_pubs(query, **search_pubs_args, start_index=start_index)
    pubs.start_index = start_index
    return pubs


def get_pubs_dummy(query, year_low=None, year_high=None, start_index=0, **kwargs):
    return DummyPubs(950, start_index)


def store_pubs(pubs, out_path=None):
    start_index = pubs.start_index
    results = []
    with (Path(out_path).open("a") if out_path else nullcontext()) as f:
        n = 0
        try:
            for n, item in enumerate(pubs):
                results.append(item)
                if f is not None:
                    f.write(json.dumps(item) + "\n")
            n += 1
        finally:
            logger.info(
                f"Start: {start_index}. Step: {n}. Restart: {start_index + n}."
                f" Last: {pubs.total_results - 1}"
            )

    return results


def store_attempt(query_args, out_path, max_results_sub=0, final=False):
    pubs = get_pubs(**query_args)
    if pubs.total_results <= (QUERY_MAX_RESULTS - max_results_sub):
        if out_path.exists():
            start_index = out_path.read_text().count("\n")
            pubs = get_pubs(**query_args, start_index=start_index)
        logger.info(query_args)
        store_pubs(pubs, out_path=out_path)
        return True
    elif final:
        raise RuntimeError("Too much monkey business!")


def store_all(out_dir=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    for term in TERMS:
        base_query = QueryBuilder.quote(term)
        for year in YEARS:
            out_path = out_dir / f"{term} - {year}"
            query_args = {
                "query": base_query,
                "year_low": year,
                "year_high": year,
                "language": "en",
                "review_only":False
            }
            # total_results is a bit fuzzy so play safe with a margin of 100
            if store_attempt(query_args, out_path, 100):
                continue
            for month in MONTHS:
                out_path = out_dir / f"{term} - {year} - {month}"
                query_args["query"] = QueryBuilder.and_(base_query, month)
                store_attempt(query_args, out_path, final=True)
            out_path = out_dir / f"{term} - {year} - None"
            query_args["query"] = QueryBuilder.and_(
                base_query, *(QueryBuilder.not_(month) for month in MONTHS)
            )
            store_attempt(query_args, out_path, final=True)


class DummyPubs(list):
    def __init__(self, total_results, start_index):
        self.start_index = start_index
        self.total_results = total_results
        self.append({})
