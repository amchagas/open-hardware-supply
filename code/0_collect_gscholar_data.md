### systematically retrieve entries from google scholar using code:

- After quite a bit of digging we learned that the only search tool/database of 
academic papers that returns keyword searches by also looking at the body of text
(and not just abstract, author and title fields) is google Scholar.
  
- However, google scholar does not like web scraping, and doing this manually 
would mean not being able to do it at all... So we found a workaround for this
based on several online tutorials. 

- to reproduce this, readers will need an account at [scraperapi](scraperapi.com)
(their free version allows 5000 requests per month, which might be enough
 for some projects). They will also need to use Python and Scrapy (if you are using
 Anaconda or miniconda, setting this up is as easy as typing 
 "conda new --name scrapy; conda activate scrapy; conda install -c conda-forge scrapy;")
 
 -We then used code from [this repo](https://github.com/ian-kerins/google-scholar-scrapy-spider) 
 to run the crawler
 
 
 spyder is run with the following command in a terminal:
 "scrapy crawl OSH -o 2021.jl"
 