#import doi as doiLib
#from unpywall.utils import UnpywallCredentials
#from unpywall import Unpywall
from prepare_wos_data_to_json import Prepare as prp
from pathlib import Path
#from tqdm.auto import tqdm


dataloc = "/home/andre/repositories/open-hardware-supply/data/method2-scholarly-data/"

locations = [#"open_labware/derived/",
             # open_source_instrument/derived/",
             # open_open_scientific_hardware/derived/",
             # open_source_instrumentation/derived/",
             # open_science_hardware/derived/",
             # open_source_hardware/derived/",
             # open_source_hardware/2005-2013/derived/",
              dataloc+"open_source_hardware/2023/derived/",
              dataloc+"open_source_hardware/2017/derived/",
              #dataloc+"open_source_hardware/2020/derived/",
             ]

#dataPath = "../data/derived/20230214/"
dataFile = "records.jsonl"



for item in locations:
    print(item)
    data = prp(source_file=item+dataFile, output_dir=item)
    data.run()
    data.save("wos_data_as.json")