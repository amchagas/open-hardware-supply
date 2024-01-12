"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api
"""

import get_wos_records_from_api as gwr
from pathlib import Path

source_files = gwr.DATA_PATHS
# output_dir ="/home/andre/repositories/open-hardware-supply/data/method2-scholarly-data/dumpdata/derived/"
output_dir = Path("../../data/method2-scholarly-data/dumpdata/derived")

try:
    api_key = Path("./wos_api_key").read_text()
except FileNotFoundError:
    api_key = input("Enter API key: ")

wosTtr = gwr.TitlesToRecords(source_files, output_dir, api_key)
wosTtr.download_records()
wosTtr.dump_records()
