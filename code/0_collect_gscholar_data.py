import calendar
from contextlib import nullcontext
import json
from pathlib import Path

from scholarly import scholarly

# Keep it simple and close to the essential terms,
# and so in the scope of claiming OSH qualities
TERMS = (
    "open hardware",
    "open source hardware",
    "opensource hardware",
    "open science hardware",
    "open scientific hardware",
    # 'open source instrument',
    # 'open source instrumentation',
)

# 2005 → Arduino, Make, Git, ...
# full_query [< 2005]: 615 results
# full_query [>=2000 & < 2005]: 335 results
YEARS = tuple(range(2005, 2023))


# Months in current locale (English if not specified)
MONTHS = tuple(calendar.month_name[m] for m in range(1, 13))


class QueryBuilder:
    @staticmethod
    def quote(x):
        return f'"{x}"'

    @staticmethod
    def or_(xs):
        return "(" + " OR ".join(xs) + ")"

    @staticmethod
    def not_(x):
        """NOTs must go at the end and outside nontrivial parenthesis"""
        return f"-{x}"

    @staticmethod
    def and_(xs):
        return "(" + " ".join(xs) + ")"


def get_full_query(terms):
    return QueryBuilder.or_(QueryBuilder.quote(term) for term in terms)


def get_pubs(query, year_low=None, year_high=None, start_index=0, **kwargs):
    search_pubs_args = {"year_low": year_low, "year_high": year_high, **kwargs}
    pubs = scholarly.search_pubs(query, **search_pubs_args, start_index=start_index)
    pubs.start_index = start_index
    return pubs


def store_pubs(pubs, out_path=None):
    start_index = pubs.start_index
    results = []
    with (Path(out_path).open("a") if out_path else nullcontext()) as f:
        try:
            for n, item in enumerate(pubs):
                results.append(item)
                if f is not None:
                    f.write(json.dumps(item) + "\n")
            n += 1
        finally:
            print(f"Start: {start_index}. Step: {n}. Restart: {start_index + n}.")

    return results


def store_all(out_dir=None):
    out_dir = Path(out_dir)
    for term in TERMS:
        for year in YEARS:
            base_query = QueryBuilder.quote(term)
            query_args = {
                "query": base_query,
                "year_low": year,
                "year_hight": year,
            }
            pubs = get_pubs(query_args)
            if pubs.total_results < 900:
                store_pubs(pubs, out_path=out_dir / f"{term} - {year}")
                continue
            for month in MONTHS:
                query_args["query"] = QueryBuilder.and_(base_query, month)
                pubs = get_pubs(query_args)
                if pubs.total_results < 900:
                    store_pubs(pubs, out_path=out_dir / f"{term} - {year} - {month}")
            query_args["query"] = QueryBuilder.and_(
                base_query, *(QueryBuilder.not_(month) for month in MONTHS)
            )
            pubs = get_pubs(query_args)
            if pubs.total_results < 900:
                store_pubs(pubs, out_path=out_dir / f"{term} - {year} - {month}")
