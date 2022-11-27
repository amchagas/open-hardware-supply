# Open hardware documentation in academic papers: Truly open, or just open washing?


Hi there! This project started because we were interested in knowing the 
quality of the documentation in peer reviewed papers describing open source 
hardware. 

In other words, are the hardware being described in papers replicable? Are the 
papers sharing enough information that would allow others to re-create/modify/adapt
the tools being described?

So we are using web scraping tools trying to collect most papers/books/
conference papers out there that have "Open Hardware" as a keyword anywhere in 
the text/title/keywords (details on the methods section below), than we clean 
up the database, and make it publicly available in [Zotero](https://www.zotero.org/groups/4871493/open_hardware_database)

With the database in place, we can filter the peer reviewed articles and start 
investigating their documentation, and scoring them according to a set of pre-defined
criteria.

Once we have analysed a set of these papers we will be in a good position to 
understand the overall documentation quality of the field, see how things evolve
over time, and if documentation quality correlates with journals.


### Methods:

We are using a couple of open source tools, plus some code of our own to collect
information about academic work related to open source hardware, namely:

0 - We use [Scrapy](https://scrapy.org/) coupled with [ScraperAPI](https://www.scraperapi.com/)
to scrape data from Google Scholar (GS). We use GS because it is to our knowledge
the only database that performs queries on the entire documents it hosts,
as oppposed to only title, abstract etc, as other databases. This combination 
allows us to systematically mine data using keywords combined with time 
periods to get a certain number of hits per query, bypassing google's "result 
output limitation" (ie only the first 1000 values being returned at each search).

1 - This generates a bit of a mountain of disorganised data, as Google Scholar 
has entries comprising books, master thesis, peer reviewed articles, etc. Plus 
not all entries comprise a Digital Object Identifier (DOI) which makes it a bit
hard to get structured metadata. To solve this, we use custom code to match
each entry from GS to the Web of Science (WOS) database. For each entry we 
use title, author and year to get matches. This gives us more structured metadata
including DOIs

2 - The WOS entries have a lot of metadata, and we use only a subset of it. In 
this step we structure the data to have only this subset of the metadata for all
entries, and prepare it to run through the Unpaywall API.

3 - Using the Unpaywall API, we can get information about whether or not each 
entry is published as open access(OA) or not, and what kind of OA it is (Green,
Gold, Hybrid, etc).

4 - Once we have collected all above information, we can use DOIs and the 
Zotero translation server to systematically add the entries to a public Zotero
collection.

5 - Within Zotero, we can comb through the articles we are interested in and 
score the quality of their documentation based on the classification system
described on the Open-O-Meter. This would give a well documented paper a total
score of 8 out of 8. We add another point to this classification based on 
an entry being open access (so, end up with 9 points for well documented papers). 

Hi! This project is a side interest to see how/if open source hardware(OSH) is being adopted in Academia. 

To do that, we are using Web of Science tools, as well as manual tracking to see/check things like:
- number of papers describing OSH increases over time (initially over 2000-2020 period)
- where they are being published
  - academic journals, conference proceedings, news, highlights? what would be the other?
- if they are released as preprints
- what percentage includes links to hardware documentation
  - how do journal practices and other factors impact the prevalence and quality of such
- number of citations these papers get
- etc.

Results will eventually be published as a paper [currently under construction](https://docs.google.com/document/d/11K1XJKBIxdgYoO2fNESj3t8K9d_UI31NhEpDk5qaYH0/edit?usp=sharing)

----

## Methods:

### Tools used

- [Zotero](<https://www.zotero.org/>)
- [Python3](<https://www.python.org/>)
- [rxivist](<https://rxivist.org/docs>) ?

### Python libraries used
- evolving; check the code

### databases used
- evolving; check the code

- [Web of Science](<webofknowledge.com>)
- [Scopus](<https://www.scopus.com/>)
- [BioRxiv](<https://www.biorxiv.org/>) ?
- [Google Scholar](<https://scholar.google.com/>) ?

- Data from the discontinued [PLOS Open Source Toolkit](https://collections.plos.org/collection/open-source-toolkit-hardware/)

### Data collection 

- Manual tracking with google scholar alerts

- Data obtained from scholarly databases using [a search query](code/project_definitions.py) and exported in RIS format

- Once cleaned and harmonized it is imported in Zotero so that users can curate/annotate the data, mainly checking:
  - if the papers were released with design files (either as a repository and/or supplemental files in the paper)
  - if the papers were released as preprints before being published as peer-reviewed articles.

### Data presentation

- data is analysed with Python 3 using Jupyter Notebook
  
---

## Onboarding

If you would like to contribute to this project, please create an issue.


## Old instructions (out of date)

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


### help needed right now (also out of date)

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

---

## Collaborators (alphabetic order)

- Alexandre Hannud Abdo
- Andre Maia Chagas (project lead)
- Matias Andina
- Miguel Fernandes
- Natasha Pouchkina-Stantcheva
- Tom Baden
