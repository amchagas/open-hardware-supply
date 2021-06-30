# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime


API_KEY = open('scraperapi_api_key').read().strip()


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url} #'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class ExampleSpider(scrapy.Spider):
    name = 'OSH'
    allowed_domains = ['api.scraperapi.com']

    def start_requests(self):
        begYear = str(2021)
        endYear = str(2021)
        start = 0
        position = start
        month1 = "January OR February OR March OR April OR June"
        month2 =  "July OR August OR September OR October OR November OR December"
        monthIndex = 0
        queries = ['"open hardware" ']#+month2]#,'"open hardware" '+month2 ]
        #queries = ['"open * hardware"'+"AND "+month[monthIndex] ]
        #"""
        # OR "open labware" OR "open source equipment" OR "open source hardware" OR \
        #    "open source labware" OR "open source design" OR "opensource equipment" OR "opensource hardware" OR "opensource labware" OR \
        #    "opensource design" OR "open science equipment" OR "open science hardware" OR "open science labware" OR "open science design" OR \
        #    "frugal equipment" OR "frugal hardware" OR "frugal labware" OR "frugal design" OR "free hardware and software"'
        #"""

        
        for query in queries:
            print(" ")
            print("query: "+str(query))
            print(" ")
            url = 'https://scholar.google.com/scholar?' + urlencode({'hl': 'en',
             'q': query,
             'as_vis':"1", # this removes the display of citations
             'start':str(start), # position where to start collection data. if the api drops, one can restart from where it stopped.
             'as_ylo':begYear,
             'as_yhi':endYear,
             'num': '20' # set the number of results per page, on GS either 10 or 20. Under the impression that setting to 20 decreases the number of API calls. 
             })
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': position})

    def parse(self, response):
        print("\n")
        print(response.url)
        print("\n")
        ##print("\n")
        #print(dir(response))
        #print("\n")            
        
        #for key in response.meta.keys():
        #    print("\n")
        #    print(key)
        #    print("\n")            
            
        position = response.meta['position']
        for res in response.xpath('//*[@data-rp]'):
            link = res.xpath('.//h3/a/@href').extract_first()
            temp = res.xpath('.//h3/a//text()').extract()
            if not temp:
                title = "[C] " + "".join(res.xpath('.//h3/span[@id]//text()').extract())
            else:
                title = "".join(temp)
            snippet = "".join(res.xpath('.//*[@class="gs_rs"]//text()').extract())
            cited = res.xpath('.//a[starts-with(text(),"Cited")]/text()').extract_first()
            temp = res.xpath('.//a[starts-with(text(),"Related")]/@href').extract_first()
            related = "https://scholar.google.com" + temp if temp else ""
            num_versions = res.xpath('.//a[contains(text(),"version")]/text()').extract_first()
            published_data = "".join(res.xpath('.//div[@class="gs_a"]//text()').extract())
            position += 1
            print("\n")
            print("position" + str(position))
            print("\n")
            item = {'title': title, 'link': link, 'cited': cited, 'relatedLink': related,
                    'position': position,
                    'numOfVersions': num_versions, 
                    'publishedData': published_data,
                    'snippet': snippet}
            yield item
        next_page = response.xpath('//td[@align="left"]/a/@href').extract_first()
        print("\n")
        print("next page: "+str(next_page)) 
        print("\n")
        if next_page:
            url = "https://scholar.google.com" + next_page
            yield scrapy.Request(get_url(url), callback=self.parse,meta={'position': position})
