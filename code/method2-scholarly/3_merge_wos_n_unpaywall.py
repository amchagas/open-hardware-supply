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


dataRoot = "/home/andre/repositories/open-hardware-supply/data/method2-scholarly-data/"

logging.basicConfig(filename=dataRoot+"doierrors.txt",level=logging.DEBUG)
logging.captureWarnings(True)


terms = [#"open_labware",
         #"open_source_instrument",
         #"open_scientific_hardware",
         #"open_source_instrumentation",
         #on"open_source_hardware",
         #"open_science_hardware",
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

for key in locations.keys():
    allData = pd.DataFrame()
    for dataPath in locations[key]:
        with open(dataPath+"/"+dataFile,"r") as fid:
            dataDict = json.load(fid)
            #convert dictionary to panda dataframe
            dataPD  = pd.DataFrame.from_dict(dataDict)
            allData =pd.concat([allData,dataPD])


    savePath = dataPath[0:dataPath.find("/"+key)+len(key)+2]
    print(savePath)
    temp = list(allData["doi"])
    dois = [i for i in temp if i is not None]
    #dois = allData["doi"][allData["doi"]!=None]
    #dois = list(dois)
    #for idx,item in enumerate(dois):
    #    if item == None:
    #        #dois[idx]="none"
    #        dois.pop(idx)
    #upwData = 
    index = 0
    errors=list()
    for index,doi in enumerate(dois):
        try:
            onePoint = Unpywall.doi(dois=[doi],errors="ignore")#,progress=True)
            time.sleep(0.1)
            print(index)
            if index==0:
                upwData=onePoint
            else:
                if onePoint is not None:
                    onePoint.index=[index]
                    upwData = pd.concat([upwData,onePoint])
        #except HTTPError:
        #    errors.append(doi)
        finally:
            errors.append(doi)
    #upwData = Unpywall.doi(dois=dois,errors="ignore",progress=True)
    
    upwData.to_json(savePath+key+"_upwData.json")

#upwJson = upwData.to_json()
#parsed = json.loads(upwJson)
#with open(dataPath+"upwData.json","w") as fid:
#    upwData.to_json(fid)

#articles = pd.merge(wosArticles, upwData,on="doi" )
#articles.to_json(dataPath+"articles_to_review")

#Open Access

#Paper distribution 
#print(articles.oa_status.value_counts(normalize=True))
#print(articles.oa_status.value_counts(normalize=False))
#sns.histplot(data = articles.is_oa)


#entryType = list()
#for item in data["pubType"]:
#    if type(item)==str:
#        if item == "Article" or item == "Journal Article" or item == "Conference Paper":
#            entryType.append(True)
#        else:
#            entryType.append(False)
#    else:
#        #print(item)
#        if "Article" in item or "Journal Article" in item or "Conference Paper":
#            entryType.append(True)
#        else:
#            entryType.append(False)