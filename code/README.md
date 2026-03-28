## Data collection
### Folder `method2-scholarly`
#### Google Scholar
Use [Scholarly](Scrapy) with [ScraperAPI](https://www.scraperapi.com/) to scrape data from Google Scholar (GS). Use GS because it perhaps the only easily accessible database that performs queries on the entire documents it hosts, as opposed to only title, abstract.

Combine keywords with time markers to divide the number of hits per keyword query, bypassing Google's "result output limitation", i.e. only the first 1000 values being returned for a search.

#### Web of Science
1. This generates an amass of disorganized data including books and chapters, master and doctoral theses, preprints and peer reviewed articles etc. And not all entries include a Digital Object Identifier (DOI), complicating the task of obtaining structured metadata.

To solve this, match each entry from GS with the Web of Science (WOS) database, using title, author and year to get matches. WOS is queried programmatically through the API using [bibliodbs](https://gitlab.com/cortext/cortext-libraries/bibliodbs). This gives us structured metadata including DOIs

#### Unpaywall
Use the Unpaywall database through its API and from the DOI get information about whether or not each entry is published as open access (OA) or not, and what kind of OA is it (Gold, Hybrid, Green, Diamond etc).

#### Zotero
Use DOIs and the Zotero translation server to automatically add all collected entries to a Zotero group. For this group, read access is made public and write access is restricted to admins.
