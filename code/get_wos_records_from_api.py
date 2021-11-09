#!/usr/bin/env python

from pathlib import Path
import json
import httpx
import re
import time
from jellyfish import damerau_levenshtein_distance as edit_distance
from tqdm.auto import tqdm

WOS_API = "https://wos-api.clarivate.com/api/wos"
DATA_DIR = Path("/home/eris/Projects/gosh/open-hardware-supply/data/scrapy")
DATA_FILES = [
    DATA_DIR / file
    for file in [
        "open_hardware_2005-2010.jl",
        "open_hardware_2011-2013.jl",
        "open_hardware_2014.jl",
        "open_hardware_2015.jl",
        "open_hardware_2016.jl",
        "open_hardware_2017.jl",
        "open_hardware_2018.jl",
        "open_hardware_2019.jl",
        "open_hardware_2020.jl",
        "open_hardware_2021.jl",
    ]
]

DEBUG_LOG = True


class TitlesToRecords:
    def __init__(self, source_files, output_dir, api_key):
        self.api_key = api_key
        self.source_files = [Path(file) for file in source_files]
        self.store = Path(output_dir)
        self.store.mkdir(parents=True, exist_ok=True)
        self.multi_records_file = self.store / "multi_records.jsonl"
        self.records_file = self.store / "records.jsonl"
        self.normalize_rex = re.compile(r"\W+")
        self.query_fields = ["title", "pubyear", "first_author"]
        self._debug_log = []
        self._last_title = None

    def normalize_text(self, text):
        return self.normalize_rex.sub(" ", text).strip().lower()

    def debug_log(self, kind, data):
        if DEBUG_LOG:
            self._debug_log.append((kind, data))

    def scraped_data(self):
        skipping = bool(self._last_title)
        for file in tqdm(self.source_files):
            with file.open() as f:
                total = len(list(f.readlines()))
            for line in tqdm(file.open().readlines(), total=total, desc=" "):
                scraped = json.loads(line)
                data = {}

                data["title"] = self.normalize_text(scraped["title"])

                data["first_author"] = (
                    scraped["publishedData"].split("-")[0].split(",")[0].split()[-1]
                )

                if pubyear := re.search(r"\b\d{4}\b", scraped["publishedData"]):
                    data["pubyear"] = int(pubyear.group())
                else:
                    self.debug_log("Missing year", scraped)

                data["_line"] = line

                if skipping and data["title"] == self._last_title:
                    skipping = False
                    tqdm.write(f"Starting from: {self._last_title}")
                if skipping:
                    continue

                yield data

    def build_query(self, data):
        tag = {"title": "TI", "first_author": "AU", "pubyear": "PY"}
        query = [
            f"{tag[key]}=({escaped_value})"
            for key, value in data.items()
            for escaped_value in [
                " ".join(f'"{x}"' for x in value.split()) if key == "title" else value,
            ]
            if key in self.query_fields
        ]
        self.debug_log("Query", query)
        return " AND ".join(query)

    def get_records_from_scraped_data(self, data):
        query = self.build_query(data)
        headers = {
            "X-ApiKey": self.api_key,
        }
        params = {
            "databaseId": "WOK",
            "usrQuery": query,
            "count": 5,
            "firstRecord": 1,
        }
        r = httpx.get(WOS_API, params=params, headers=headers)
        time.sleep(1)
        recs = r.json()["Data"]["Records"]["records"]
        if recs:
            recs = recs["REC"]
        else:
            recs = []
            self.debug_log("Failed query", {"Parameters": params, "Text": r.text})
        return recs

    def download_records(self):
        self.multi_records_file.touch()
        with open(self.multi_records_file, "r") as rf:
            multi_records = [tuple(json.loads(x)["scraped"]) for x in rf.readlines()]
        with open(self.multi_records_file, "a") as rf:
            for data in self.scraped_data():
                data_key = tuple(data.items())
                if data_key not in multi_records:
                    recs = self.get_records_from_scraped_data(data)
                    if recs:
                        rf.writelines(
                            [json.dumps({"scraped": data_key, "records": recs}), "\n"]
                        )
                    self._last_title = data["title"]

    def check_record(self, recs, data):
        for rec in recs:
            debug = {}

            (rec_title,) = [
                x
                for x in rec["static_data"]["summary"]["titles"]["title"]
                if x["type"] == "item"
            ]
            rec_title = self.normalize_text(rec_title["content"])
            data_title = data["title"]
            title_distance = edit_distance(rec_title, data_title)
            if title_distance > 5:
                continue
            elif title_distance > 0:
                debug["Bad title"] = (rec_title, data_title)
            else:
                debug["Good title"] = data_title

            rec_authors = [
                x.get("last_name", x["full_name"].split(",")[0]).strip()
                for x in rec["static_data"]["summary"]["names"]["name"]
                if "last_name" in x or "full_name" in x
            ]
            author_distance = min(
                edit_distance(data["first_author"], author) for author in rec_authors
            )
            if author_distance > 2:
                continue
            elif author_distance > 0:
                debug["Bad author"] = (rec_authors, data["first_author"])
            else:
                debug["Good author"] = data["first_author"]

            if "pubyear" in data:
                rec_pubyear = rec["static_data"]["summary"]["pub_info"]["pubyear"]
                pubyear_distance = abs(rec_pubyear - data["pubyear"])
                if pubyear_distance > 1:
                    continue
                elif pubyear_distance > 0:
                    debug["Bad pubyear"] = (rec_pubyear, data["pubyear"])
                else:
                    debug["Good pubyear"] = data["pubyear"]

            if any(x.startswith("Bad") for x in debug):
                for key, value in debug.items():
                    self.debug_log(key, value)
            return rec

        return None

    def dump_records(self):
        with open(self.multi_records_file, "r") as mrf:
            multi_records = [tuple(json.loads(x)["scraped"]) for x in mrf.readlines()]
        self.records_file.touch()
        with open(self.records_file, "r") as rf:
            records = [tuple(json.loads(x)["scraped"]) for x in rf.readlines()]
        with open(self.records_file, "a") as rf:
            for data_key, records in multi_records:
                if data_key not in records:
                    rec = self.check_record(records, dict(data_key))
                    if rec:
                        rf.writelines(
                            [json.dumps({"scraped": rec_key, "record": rec}), "\n"]
                        )
                    self._last_title = data["title"]
