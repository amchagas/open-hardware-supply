# Tracking open source hardware in academic papers

Hi! This project is a side interest to see how/if open source hardware(OSH) is being adopted in Academia. 

To do that, we are using Web of Science tools, as well as manual tracking to see check things like:
- number of papers describing OSH increases over time
- where they are being published
- if they are released as preprints
- what percentage includes links to hardware documentation
- number of citations these papers get
- etc.

## Methods:

### Tools used

- [Zotero](https://www.zotero.org/)
- [Python3](https://www.python.org/)
- [Web of Science](webofknowledge.com)
- [Google Scholar](https://scholar.google.com/) 

### Data collection 

- Manual tracking with google scholar alerts
- getting data available from Web of Science using the following search term:
  
  
  ``` 
  TOPIC= ("Open hardware" OR "open source hardware" OR "open science hardware" OR "open labware" OR "free and open source hardware") OR TITLE= ("Open hardware" OR "open source hardware" OR "open science hardware" OR "open labware" OR "free and open source hardware")
  Timespan: All years. Indexes: SCI-EXPANDED, SSCI, A&HCI, CPCI-S, CPCI-SSH, BKCI-S, BKCI-SSH, ESCI, CCR-EXPANDED, IC.  
  ```


- Data is exported as Bibtex format and imported in Zotero.

- Zotero is then used to curated/annotate the data, together with some python scripts.


### Data presentation

- data is analysed with Python 3 using Jupyter Notebook
  


#### Onboarding

If you would like to contribute to this project you'll need to:

- Install [Zotero](https://www.zotero.org/) on your computer.
- get access to the collection by visiting https://www.zotero.org/groups/2485390/osh_evolution and asking for access
- download it to your machine
- make changes and sync with the online collection
- Collection structure:
  - "checked" contains all entries that have already been checked. Sub folders there are for each contributor, so that they can avoid duplicated work, and potential differences/errors tracked
  - "checked entries old" are old checks. This is for archival purposes only.
  - "implications of OSH" are for papers/work discussing OSH but not actually describing a new piece of OSH.
  - "Scielo" is the raw data from the Scielo database, using the same search terms described above.
  - "Medline" is the raw data from the Medline database, using the same search terms described above.
  - "Web of Science Raw" is the raw data from the Web of Science core database.
  - "staging" contains entries that are up for work. They have already been checked and are not duplicates, they are just not yet manually classified.


#### help needed right now

- we need to classify the papers, and as far as we know this has to be done manually. So we are using Zotero to manually annotate the papers with Tags:

  - If a paper has a repository or a web resource (supplemental information section for instance) with more documentation containing files that can be used to reproduce the device it gets the 'repository' tag, and nothing otherwise.
    - keywords used to find the repositories/extra information:
        available, github, code, supplemental, shared, download, gitlab, repository 


  
  - We would also like to know if a paper was published previously as a preprint, in case it was, add "alsopreprint" tag
  
  - We would also like to know if a paper was a conference poster/abstract, in case it was, add "alsoconference" tag
  
  (the following tags might be easy to implement as python scripts since most of these are in the bib file (but not in Zotero), I would avoid working on them right away)

  - We would also like to classify the paper based on their fields (more than one can be added):
    - Neuroscience
    - Molecular Biology
    - Environmental Sciences
    - Life Sciences
    - Chemistry
    - Engineering