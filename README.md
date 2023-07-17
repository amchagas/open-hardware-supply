
# Practices vs. standards of Open Hardware documentation in academic papers: adoption barriers and open washing


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


Results will placed here and also as a preprint and then submitted peer-review.


---

## Collaborators (alphabetic order)

- Alexandre Hannud Abdo
- Andre Maia Chagas (project lead)
- Heba Nashid
- Matias Andina
- Miguel Fernandes
- Natasha Pouchkina-Stantcheva
- Tom Baden



--- 

#### keywords used to exclude URLs from PDF mining:

- orcid
- nih



####  keywords used to include URLs from PDF mining:
- mendeley
- osf
- github
- gitlab
- .zip
