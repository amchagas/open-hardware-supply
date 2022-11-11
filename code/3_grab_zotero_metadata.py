"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api
"""
import requests
import pandas as pd
from pyzotero import zotero
import json
import time


dataPath = "../data/derived2/"
dataFile = "upwData.json"
articles = pd.read_json(dataPath + dataFile)

dois = list(set(articles.doi))
##to run zotero translator, one needs to have docker installed and run it so (if one is using command line):
#docker pull zotero/translation-server
#docker run -d -p 1969:1969 --rm --name translation-server zotero/translation-server


url = "http://127.0.0.1:1969/search"  # zotero translator server running locally
headers = {"content-type": "text/plain", "Accept-Charset": "UTF-8"}
# r = requests.post(url=url, data=dois[0], headers=headers)


allMeta = list()
for item in dois:
    r = requests.post(url=url, data=item, headers=headers)
    allMeta.append(r.json())
    r.close()

with open(dataPath + "zotMeta.json", "w") as fid:
    json.dump(allMeta, fid)



with open(dataPath + "zotMeta.json", "r") as fid:
    allMeta = json.load(fid)
# print(data)

with open("zotero_api","r") as fid:
    key = fid.readline()

zot = zotero.Zotero(library_id=4851522,library_type='group', api_key=key)

index=0
for item in allMeta:
    index=index+1
    zot.create_items(item)
    time.sleep(1)
    print(index)

