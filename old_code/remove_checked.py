import pandas as pd


checked = pd.read_csv("checked.csv")
notchecked = pd.read_csv("hardware_web_science.csv")


# index of publications (the dataset also has webpages, conference papers, etc)
pubIndex1 = checked[checked["Item Type"] == "journalArticle"].index

checkedTitles = checked["Title"]

notCheckedTitles = notchecked["Title"]
len(notCheckedTitles)
len(checkedTitles)
[i for e in notCheckedTitles for i in checkedTitles if e in i]


pubIndex2 = notchecked[notchecked["Item Type"] == "journalArticle"].index

notCheckedArticles = notchecked.loc[pubIndex2]


len(checkedArticles)

len(notCheckedArticles)

len(notchecked)