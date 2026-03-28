# Open Hardware knowledge practices in academic publications: what is? what matters?

We're investigating the quality of knowledge in peer reviewed papers describing open source hardware. Are the hardware being described replicable?  Are papers sharing enough information that would allow others to build/modify/adapt the tools described?  Do interested users find appropriate channels to learn and contribute?

We have collected thousands of full-text papers mentioning “open hardware” using automated methods, listed in [this Zotero database](https://www.zotero.org/groups/4871493/open_hardware_database). And we're now scoring a representative sample of articles using an instrument called the [Open-o-Meter](https://doi.org/10.1016/j.procir.2018.08.306).

The results of our coding effort will enable asking a number of important questions for the field, such as how good is documentation in general? For what criteria is it most and least open? How such qualities have evolved over time? And whether documentation quality has improved with openness policies adopted by certain journals?

Please get in touch if you want to contribute!


## Tasks
- Confirm scholarly still works
- Re-run scholarly code to collect data from 2025, 2024, 2023
- Re-run scholarly code to re-collect data from previous years?
- Calculate sample with stratification by year
- Sample publications to be coded
- Code publications

## Data
### Acquired
- Bibliographic records A
    - Count: 1k
    - Span: 19xx-2020
    - Source: Google Scholar, Web of Science
    - Procedure: Scrapy, ScraperAPI
    - Storage: Zotero group "hardware_web_science"

- Bibliographic records B
    - Count: 3k
    - Span: 19xx-2022
    - Source: Scholarly, ScraperAPI
    - Storage: Zotero group "open_hardware_database"

- Full text files
    - Type: PDF
    - OA: True
    - Count: 1244
    - Source: Unpaywall
    - Source: Bibliographic records B
    - Storage: GIN repository

### Desired
- Bibliographic records B+
    - Span: 2023-2025
    - Count: ?
    - Source: scholarly
    - Storage: Zotero group "open_hardware_database"

- Full text files
    - Type: PDF
    - OA: True
    - Count: ?
    - Source: Unpaywall
    - Input: Bibliographic records B+
    - Storage: GIN repository


## Coding publications
### Criteria
- Base: Open-O-Meter
- Adaptations: Open access, Community spaces
- Definition: See our [Codebook](/docs/codebook.md)

### Corpus
- Representative sample of publications
- Stratified by year


## Hypotheses
1. number of published open hardware articles increases in relation to previous year

1. Quality of open hardware documentation improves over time (as more guidelines and work is done in the field, with new licenses, documentation platforms and the surge of a community)

1. Do journal policies correlate with higher openness ?

1. Journal field should not correlate with documentation quality (except those dedicated for open hardware)

1. Documentation quality should not be correlated with Open access & non-open articles 

1. JOH & HX: how they compare to each other and to the overall pool?

### Excess hypotheses
- Does open peer review impact quality?
- What new questions can we ask with access to reviewer's comments?
- Are there elements of the documentation that would hint towards long term design sustainability? in other words are there documentation elements that indicate if a design is going to remain an open hardware prototype, or if it is going to evolve towards being an open hardware product?


## Data collection
1. Use [Scholarly](Scrapy) with [ScraperAPI](https://www.scraperapi.com/) to scrape data from Google Scholar (GS). Use GS because it perhaps the only easily accessible database that performs queries on the entire documents it hosts, as opposed to only title, abstract.

Combine keywords with time markers to divide the number of hits per keyword query, bypassing Google's "result output limitation", i.e. only the first 1000 values being returned for a search.

1. This generates an amass of disorganized data including books and chapters, master and doctoral theses, preprints and peer reviewed articles etc. And not all entries include a Digital Object Identifier (DOI), complicating the task of obtaining structured metadata.

To solve this, match each entry from GS with the Web of Science (WOS) database, using title, author and year to get matches. This gives us structured metadata including DOIs

1. Use the Unpaywall database through its API and from the DOI get information about whether or not each entry is published as open access (OA) or not, and what kind of OA is it (Gold, Hybrid, Green, Diamond etc).

1. Use DOIs and the Zotero translation server to automatically add all collected entries to a Zotero group.

For this group, read access is made public and write access is restricted to admins.


## Collaborators (αβ)
- [Alexandre Hannud Abdo](https://orcid.org/0000-0002-4849-4631)
- [Andre Maia Chagas](https://orcid.org/0000-0003-2609-3017) (project lead)

### Former collaborators
- Anton Vasiljevs
- Heba Nashid
- Matias Andina
- Miguel Fernandes
- Natasha Pouchkina-Stantcheva
- Tom Baden
