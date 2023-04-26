"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api

uses pyZotero library
Stephan Hügel, The Pyzotero Authors (2019, May 18). urschrei/pyzotero: Version v1.3.15. http://doi.org/10.5281/zenodo.2917290

also uses zotero translator server via docker.
to run zotero translator, one needs to have docker installed and run it so (if one is using command line):

#docker pull zotero/translation-server
#docker run -d -p 1969:1969 --rm --name translation-server zotero/translation-server

"""
import requests
import pandas as pd
from pyzotero import zotero
#import json
#import time


dataPath = "../data/derived/20230214/"
dataFile = "upwData.json"
articles = pd.read_json(dataPath + dataFile)
#idx = set(articles.doi)

url = "http://127.0.0.1:1969/search"  # zotero translator server running locally
headers = {"content-type": "text/plain", "Accept-Charset": "UTF-8"}
# r = requests.post(url=url, data=dois[0], headers=headers)




with open("zotero_api","r") as fid:
    key = fid.readline()

zot = zotero.Zotero(library_id=4871493,library_type='group', api_key=key)

#grab all existing entries on the database
numItems = zot.count_items()
allPrevious = zot.everything(zot.top())

#compare to Unpaywall entries and index entries already present in the zotero 
#collection
existing = list()
for item in allPrevious:
    try:
        existingDoi = item["data"]["DOI"]
        if len(articles[articles["doi"]==existingDoi].index)>0:
            existing.append(articles[articles["doi"]==existingDoi].index.values[0])
        
    except KeyError:
        print("no doi in this entry")


#drop the entries that are already present on the zotero collection
if len(existing)>0:
    articles = articles.drop(labels=existing,axis=0)




# now add entries to the zotero collection, add the type of OA to tags
index=0
#allMeta = list()
for idx in articles.index:
    try:
        r = requests.post(url=url, data=articles["doi"][idx], headers=headers)
        temp = r.json()
        r.close()
        
        #temp[0]["tags"].append(articles["oa_status"][idx])
        
        zot.create_items(temp)
        zot.add_tags(zot.item(temp[0]["key"]),articles["oa_status"][idx])
        index=index+1
        print(index)

        #time.sleep(0.5)

    except:
        print(articles["doi"][idx])
        print(r)
        print(r.reason)
        
        
        
        



#for item in allMeta:
#    if item !="None":
        

#        time.sleep(1)
        
#with open(dataPath + "zotMeta.json", "w") as fid:
#    json.dump(allMeta, fid)



#with open(dataPath + "zotMeta.json", "r") as fid:
#    allMeta = json.load(fid)
 
 #print(data)


#zotTitles = list()
#for item in allPrevious:
#    try:
#        zotTitles.append(item["data"]["title"])
#    except KeyError:
#        print(item["data"]["itemType"])

#allMetaTitles = list()

#for item in allMeta:
#    try:
#        print(item[0]["title"])
#        allMetaTitles.append(item[0]["title"])
#    except TypeError:
#        print(item)




