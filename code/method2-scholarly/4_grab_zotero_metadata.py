"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api

uses pyZotero library
Stephan Hügel, The Pyzotero Authors (2019, May 18). urschrei/pyzotero: Version v1.3.15. http://doi.org/10.5281/zenodo.2917290

also uses zotero translator server via docker.
to run zotero translator, one needs to have docker installed and run it so (if one is using command line):

docker pull zotero/translation-server
docker run -d -p 1969:1969 --rm --name translation-server zotero/translation-server

"""
import requests
import pandas as pd
from pyzotero import zotero
import logging
#import json
import time
import urllib

dataRoot = "/home/andre/repositories/open-hardware-supply/data/method2-scholarly-data/"
logging.basicConfig(filename=dataRoot+"translator_errors.txt",level=logging.DEBUG)
logging.captureWarnings(True)

useEachTerm = False

if useEachTerm:
    
    terms = [#"open_labware",
        #"open_source_instrument",
        #"open_scientific_hardware",
        #"open_source_instrumentation",
        #"open_source_hardware",
        #"open_science_hardware",
        "open_hardware",
        ]


    dataLoc = list()

    for term in terms:
       #dataPath = dataRoot
       dataFile = term+"/"+"wos_upwData_combined.json"
       dataLoc.append(dataRoot + dataFile)

    articles = pd.DataFrame()
    for item in dataLoc:
        data = pd.read_json(item)
        articles = pd.concat([articles,data],ignore_index=True)
     
    
else:
    allCombName = "allWosEntries_combined_raw.json"
    articles = pd.read_json(dataRoot+allCombName)
    

#remove duplicates (ie articles that were found more than once by the queries of different terms
articles = articles.drop_duplicates(subset='doi', keep="first")
# r = requests.post(url=url, data=dois[0], headers=headers)




with open("zotero_api","r") as fid:
    key = fid.readline()
# 
zot = zotero.Zotero(library_id=4871493,library_type='group', api_key=key)
# 
# #grab all existing entries on the database
numItems = zot.count_items()


allPrevious = zot.everything(zot.top())


#compare to Unpaywall entries and index entries already present in the zotero 
#collection
existing = list()
for item in allPrevious:
    try:
        existing.append(item["data"]["DOI"])

        
    except KeyError:
        print("no doi in this entry")


#drop the entries that are already present on the zotero collection
if len(existing)>0:
    for item in existing:
        articles = articles.drop(articles[articles.doi==item].index)



# Zotero translator server running locally
url = "http://127.0.0.1:1969/search"
headers = {'Content-Type': 'text/plain',}
# Now add entries to the zotero collection, add the type of OA to tags
#index=0
#allMeta = list()
for idx in articles.index:
    print(articles["doi"][idx])
    
    r = requests.post(url=url, data=articles["doi"][idx],
                      headers=headers)

    print(r.status_code)        
    #print(r.text)
    
    
    time.sleep(1)
    #r.close()
    if r.status_code== 200:
        temp = r.json()    
        zot.create_items(temp)
    
    r.close()   
        
#         
#         
# 
# 
# 
# #for item in allMeta:
# #    if item !="None":
#         
# 
# #        time.sleep(1)
#         
# #with open(dataPath + "zotMeta.json", "w") as fid:
# #    json.dump(allMeta, fid)
# 
# 
# 
# #with open(dataPath + "zotMeta.json", "r") as fid:
# #    allMeta = json.load(fid)
#  
#  #print(data)
# 
# 
# #zotTitles = list()
# #for item in allPrevious:
# #    try:
# #        zotTitles.append(item["data"]["title"])
# #    except KeyError:
# #        print(item["data"]["itemType"])
# 
# #allMetaTitles = list()
# 
# #for item in allMeta:
# #    try:
# #        print(item[0]["title"])
# #        allMetaTitles.append(item[0]["title"])
# #    except TypeError:
# #        print(item)
# 
# 
# 

