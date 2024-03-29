#import doi as doiLib
#from unpywall.utils import UnpywallCredentials
#from unpywall import Unpywall
from prepare_wos_data_to_json import Prepare as prp


dataPath = "../data/derived/20230214/"
dataFile = "records.jsonl"

data = prp(source_file=dataPath+dataFile, output_dir=dataPath)
data.run()
data.save("wos_data_as.json")