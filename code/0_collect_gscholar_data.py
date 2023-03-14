from contextlib import nullcontext
import json
from pathlib import Path

from scholarly import scholarly

terms = [
    "open hardware",
    "open source hardware",
    "opensource hardware",
    "open science hardware",
    "open scientific hardware",
    # 'open source instrument',
    # 'open source instrumentation',
]
queries = [f'"{term}"' for term in terms]


def get_full_query(queries):
    return " OR ".join(queries)


def store_pubs(
    query, out_path=None, year_low=None, year_high=None, start_index=0, **kwargs
):
    search_pubs_args = {"year_low": year_low, "year_high": year_high, **kwargs}
    result_iter = scholarly.search_pubs(
        query, **search_pubs_args, start_index=start_index
    )
    results = []
    with (Path(out_path).open("a") if out_path else nullcontext()) as f:
        try:
            for n, item in enumerate(result_iter):
                results.append(item)
                if f is not None:
                    f.write(json.dumps(item) + "\n")
            n += 1
        finally:
            print(f"Start: {start_index}. Step: {n}. Restart: {start_index + n}.")

    return results
