import doi as doiLib
from unpywall.utils import UnpywallCredentials
from unpywall import Unpywall
#from prepare_wos_data_to_json import Prepare as prp
import pandas as pd
import json
import seaborn as sns
import numpy as np

with open("email") as fid:
    unpaywallcred = fid.readline()

UnpywallCredentials(unpaywallcred)# could not get api cred on time, 
#so using this email which is pasted all over the web.... #unpaywallcred)

dataPath = "../data/derived2/"
dataFile = "wos_data_as.json"

with open(dataPath+dataFile,"r") as fid:
    dataDict = json.load(fid)
#convert dictionary to panda dataframe
data = pd.DataFrame.from_dict(dataDict)


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



#wosArticles = data[entryType]

dois = list(data["doi"])
for idx,item in enumerate(dois):
    if item == None:
        dois[idx]="none"

upwData = Unpywall.doi(dois=dois,errors="ignore",progress=True)
upwData.to_json(dataPath+"upwData.json")

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