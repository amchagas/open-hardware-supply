"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api
"""

import get_wos_records_from_api as gwr
from pathlib import Path

source_files =  gwr.DATA_PATHS 
output_dir ="../data/derived3"
api_key = Path('./wos_api_key').read_text()

wosTtr = gwr.TitlesToRecords(source_files,output_dir,api_key)


wosTtr.download_records()
wosTtr.dump_records()