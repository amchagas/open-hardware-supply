"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api
"""

import get_wos_records_from_api as gwr
from pathlib import Path

source_files = gwr.DATA_PATHS
# output_dir ="/home/andre/repositories/open-hardware-supply/data/method2-scholarly-data/dumpdata/derived/"

locations = [#"../../data/method2-scholarly-data/open_labware/derived",
             # "../../data/method2-scholarly-data/open_source_instrument/derived",
             # "../../data/method2-scholarly-data/open_open_scientific_hardware/derived",
             # "../../data/method2-scholarly-data/open_source_instrumentation/derived",
             # "../../data/method2-scholarly-data/open_science_hardware/derived",
              "../../data/method2-scholarly-data/open_source_hardware/2023/derived",
             # "../../data/method2-scholarly-data/open_hardware/2023/derived",
              ]
              
output_dir = Path(locations[0])

#source_files = [Path("../../data/method2-scholarly-data/dumpdata/open_labware/derived"),
#              Path("../../data/method2-scholarly-data/dumpdata/open_source_instrument/derived"),
#              Path("../../data/method2-scholarly-data/dumpdata/open_open_scientific_hardware/derived"),
#              Path("../../data/method2-scholarly-data/dumpdata/open_source_instrumentation/derived"),
#              Path("../../data/method2-scholarly-data/dumpdata/open_science_hardware/derived"),
#              Path("../../data/method2-scholarly-data/dumpdata/open_source_hardware/derived"),
#              Path("../../data/method2-scholarly-data/dumpdata/open_hardware/derived")]

try:
    api_key = Path("./wos_api_key").read_text()
except FileNotFoundError:
    api_key = input("Enter API key: ")



wosTtr = gwr.TitlesToRecords(source_files, output_dir, api_key)
wosTtr.download_records()
wosTtr.dump_records()
