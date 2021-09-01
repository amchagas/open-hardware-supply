#!/usr/bin/env python

from pathlib import Path
import json
import httpx
import re

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
    def __init__(self, api_key, target_file, source_files=DATA_FILES):
        self.api_key = api_key
        self.source_files = [Path(file) for file in source_files]
        self.target_file = Path(target_file)

    def get_titles(self):
        for file in self.source_files:
            for line in file.open().readlines():
                data = json.loads(line)
                yield data["title"]

    def get_query(self, title):
        title = title.replace('"', "")
        return f'TI=("{title}")'

    def get_record(self, title):
        query = self.get_query(title)
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
        rec = None
        try:
            rec = r.json()["Data"]["Records"]["records"]["REC"]
            self.check_record(rec, title)
            rec = rec[0]
        except Exception as e:
            rec = None
            print(f"\nFailed query: {type(e)}: {e}")
            print(f"\nParameters: {params}")
            print(f"\nText: {r.text}")

        return rec

    def check_record(self, rec, title):
        if len(rec) > 1:
            raise ValueError("Multiple results!")
        rec = rec[0]
        comp_rex = re.compile(r"\W+")
        (r_title,) = [
            x
            for x in rec["static_data"]["summary"]["titles"]["title"]
            if x["type"] == "item"
        ]
        r_title = r_title["content"]
        if comp_rex.sub(" ", r_title) != comp_rex.sub(" ", title):
            raise ValueError("No matching title!")

    def get_records(self):
        self.target_file.touch()
        with open(self.target_file, "r") as tf:
            records = [json.loads(x)["title"] for x in tf.readlines()]
        with open(self.target_file, "a") as tf:
            for title in self.get_titles():
                if title not in records:
                    rec = self.get_record(title)
                    if rec:
                        tf.writelines(
                            [json.dumps({"title": title, "record": rec}), "\n"]
                        )
                    break
