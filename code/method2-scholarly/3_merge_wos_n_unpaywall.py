from unpywall.utils import UnpywallCredentials
from unpywall import Unpywall
import pandas as pd
import json
import os
import time
import logging



with open("email") as fid:
    unpaywallcred = fid.readline()

#UnpywallCredentials.set_email(unpaywallcred)
UnpywallCredentials(unpaywallcred)# using this email which is pasted all over the web.... #unpaywallcred)


dataRoot = "/home/andre/repositories/open-hardware-supply/data/raw/method2-scholarly-data/"

logging.basicConfig(filename=dataRoot+"doierrors.txt",level=logging.DEBUG)
logging.captureWarnings(True)


terms = ["open_labware",
         "open_source_instrument",
         "open_scientific_hardware",
         "open_source_instrumentation",
         "open_source_hardware",
         "open_science_hardware",
         "open_hardware"]
locations = dict()
for item in terms:
    locations[item]=[]

dirWalk = os.walk(dataRoot)
for fullPath,_,_ in dirWalk:
    for key in locations.keys():
        if "/"+key+"/" in fullPath and "derived" in fullPath:
            locations[key].append(fullPath)


dataFile = "wos_data_as.json"
#get all data from all "wos_data_as.json" files and make one big pandas dataframe,
#including information about from which term each row came from
allData = pd.DataFrame()
for key in locations.keys():
    for dataPath in locations[key]:
        with open(dataPath+"/"+dataFile,"r") as fid:
            dataDict = json.load(fid)
            #convert dictionary to panda dataframe
            dataPD  = pd.DataFrame.from_dict(dataDict)
            dataPD["term"] = [key]*len(dataPD)
            allData =pd.concat([allData,dataPD],ignore_index=True)
            







#find doi duplicates and drop them
duplicates = allData.duplicated(subset="doi")
allDataClean = allData[~allData.duplicated(subset="doi")]
#get only valid dois:
validDois = ~allDataClean.validDoi.isna()
allDataClean = allDataClean[validDois]


allData.to_json(dataRoot+"allWosEntries_combined_raw.json")

articles=pd.DataFrame()

for key in locations.keys():
    savePath = dataRoot+key
    print(savePath)
#     print(savePath)
    dataChunk = allDataClean[allDataClean.term==key]
    dataChunk = dataChunk[~dataChunk.validDoi.isna()]
    dataChunk.index=dataChunk.index-min(dataChunk.index)
    upData = Unpywall.doi(dois=list(dataChunk.doi),
                          progress=True,
                          errors="ignore")
    combined = pd.merge(dataChunk, upData,on="doi",how="inner" )
    articles = pd.concat([articles,upData])
    upData.to_json(savePath+"_upwData.json")
    combined.to_json(savePath+"wos_upwData_combined.json") 









# 
# #Open Access
# 
# #Paper distribution 
# #print(articles.oa_status.value_counts(normalize=True))
# #print(articles.oa_status.value_counts(normalize=False))
# #sns.histplot(data = articles.is_oa)
# 
# 
# #entryType = list()
# #for item in data["pubType"]:
# #    if type(item)==str:
# #        if item == "Article" or item == "Journal Article" or item == "Conference Paper":
# #            entryType.append(True)
# #        else:
# #            entryType.append(False)
# #    else:
# #        #print(item)
# #        if "Article" in item or "Journal Article" in item or "Conference Paper":
# #            entryType.append(True)
# #        else:
# #            entryType.append(False)