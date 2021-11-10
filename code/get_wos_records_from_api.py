#!/usr/bin/env python

import httpx
import json
import logging
from pathlib import Path
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
        self.logger = self._logging()
        self._last_downloaded_title = None

    def normalize_text(self, text):
        return self.normalize_rex.sub(" ", text).strip().lower()

    def _logging(self):
        logger = logging.getLogger(f"{type(self).__module__}.{type(self).__name__}")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.store / f"{time.asctime()}.log")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        return logger

    def scraped_data(self):
        skipping = bool(self._last_downloaded_title)
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

                if pubyear := re.search(r"[,-] (\d{4}) -", scraped["publishedData"]):
                    data["pubyear"] = int(pubyear.groups()[0])
                else:
                    self.logger.debug(("Missing year", scraped))

                data["_line"] = line

                if skipping and data["title"] == self._last_downloaded_title:
                    skipping = False
                    tqdm.write(f"Starting after: {self._last_downloaded_title}")
                    continue
                if skipping:
                    continue

                yield data

    def build_query(self, data):
        tag = {"title": "TI", "first_author": "AU", "pubyear": "PY"}
        query = [
            f"{tag[key]}=({escaped_value})"
            for key, value in data.items()
            for escaped_value in [
                " ".join(f'"{x}"' for x in value.split()) if key == "title" else value
            ]
            if key in self.query_fields
        ]
        self.logger.debug(("Query", query))
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
        elif isinstance(data.get("pubyear", None), int):
            data = data.copy()
            data["pubyear"] = f'{data["pubyear"]-1}-{data["pubyear"]+1}'
            return self.get_records_from_scraped_data(data)
        else:
            recs = []
            self.logger.debug(("Failed query", {"Parameters": params, "Text": r.text}))
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
                    self._last_downloaded_title = data["title"]

    def check_record(self, recs, data):
        for rec in recs:
            debug = {}

            (rec_title,) = [
                x
                for x in rec["static_data"]["summary"]["titles"]["title"]
                if x["type"] == "item"
            ]
            rec_title = self.normalize_text(rec_title["content"])
            title_distance = edit_distance(rec_title, data["title"])
            if title_distance > 5:
                continue
            elif title_distance > 0:
                debug["Bad title"] = (rec_title, data["title"])
            else:
                debug["Good title"] = data["title"]

            rec_authors = [
                y.get("last_name", y["full_name"].split(",")[0]).strip()
                for x in [rec["static_data"]["summary"]["names"]["name"]]
                for y in (x if isinstance(x, list) else [x])
                if "last_name" in y or "full_name" in y
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
                    self.logger.debug((key, value))
            return rec
        if recs:
            self.logger.debug(("No match", data))
        return None

    def dump_records(self):
        with open(self.multi_records_file, "r") as mrf:
            multi_records = {
                tuple(tuple(x) for x in rec["scraped"]): rec["records"]
                for line in mrf.readlines()
                for rec in [json.loads(line)]
            }
        self.records_file.touch()
        with open(self.records_file, "r") as rf:
            records = [tuple(json.loads(x)["scraped"]) for x in rf.readlines()]
        with open(self.records_file, "a") as rf:
            for data_key, records in multi_records.items():
                if data_key not in records:
                    rec = self.check_record(records, dict(data_key))
                    if rec:
                        rf.writelines(
                            [json.dumps({"scraped": data_key, "record": rec}), "\n"]
                        )
