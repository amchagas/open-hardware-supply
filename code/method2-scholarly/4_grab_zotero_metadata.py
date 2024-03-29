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
import logging
#import json
#import time


dataRoot = "/home/andre/repositories/open-hardware-supply/data/raw/method2-scholarly-data/"
logging.basicConfig(filename=dataRoot+"translator_errors.txt",level=logging.DEBUG)
logging.captureWarnings(True)

terms = ["open_labware",
         #"open_source_instrument",
         #"open_scientific_hardware",
         #"open_source_instrumentation",
         #"open_source_hardware",
         #"open_science_hardware",
         #"open_hardware",
         ]

dataPath = dataRoot+terms[0]+"/"
dataFile = terms[0]+"_upwData.json"
articles = pd.read_json(dataPath + dataFile)
#idx = set(articles.doi)


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



url = "http://127.0.0.1:1969/web"  # zotero translator server running locally
#header = {"user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 my-custom-translation-server/2.0 (a.maia-chagas@sussex.ac.uk)',
#           "content-Type": "text/plain", "Accept-Charset": "UTF-8"}
#Content-Type: text/plain
header = {"content-type": "text/plain", "accept-charset": "UTF-8"}
#headers = {'User-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

# now add entries to the zotero collection, add the type of OA to tags
#index=0
#allMeta = list()
for idx in articles.index:
    try:
        
        r = requests.post(url=url, data="https://doi.org/"+articles["doi"][idx], headers=header)
        #print(r.text)
        temp = r.json()
        r.close()
        
        #temp[0]["tags"].append(articles["oa_status"][idx])
        
        zot.create_items(temp)
        zot.add_tags(zot.item(temp[0]["key"]),articles["oa_status"][idx])
        #index=index+1
        #print(index)

        #time.sleep(0.5)

    except:
        print(articles["doi"][idx])
        #print(r.text)
        #print(r.reason)
        
        
        
        



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




