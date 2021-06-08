# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime

API_KEY = '8f4fae079ce11e1df2cb8ed31f9c706c'

def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'gb '}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class ExampleSpider(scrapy.Spider):
    name = 'OSH'
    allowed_domains = ['api.scraperapi.com']

    def start_requests(self):
        queries = ['"open hardware"' ]
        """
        OR "open hardware" OR "open labware" OR "open source equipment" OR "open source hardware" OR \
            "open source labware" OR "open source design" OR "opensource equipment" OR "opensource hardware" OR "opensource labware" OR \
            "opensource design" OR "open science equipment" OR "open science hardware" OR "open science labware" OR "open science design" OR \
            "frugal equipment" OR "frugal hardware" OR "frugal labware" OR "frugal design" OR "free hardware and software"'
        """
        for query in queries:
            url = 'https://scholar.google.com/scholar?' + urlencode({'hl': 'en', 'q': query,'start':'650'})
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': 0})

    def parse(self, response):
        #print(response.url)
        position = response.meta['position']
        for res in response.xpath('//*[@data-rp]'):
            link = res.xpath('.//h3/a/@href').extract_first()
            temp = res.xpath('.//h3/a//text()').extract()
            if not temp:
                title = "[C] " + "".join(res.xpath('.//h3/span[@id]//text()').extract())
            else:
                title = "".join(temp)
            #snippet = "".join(res.xpath('.//*[@class="gs_rs"]//text()').extract())
            cited = res.xpath('.//a[starts-with(text(),"Cited")]/text()').extract_first()
            temp = res.xpath('.//a[starts-with(text(),"Related")]/@href').extract_first()
            related = "https://scholar.google.com" + temp if temp else ""
            #num_versions = res.xpath('.//a[contains(text(),"version")]/text()').extract_first()
            published_data = "".join(res.xpath('.//div[@class="gs_a"]//text()').extract())
            position += 1
            print("position" + str(position))
            item = {'title': title, 'link': link, 'cited': cited, 'relatedLink': related, 'position': position,
                    #'numOfVersions': num_versions, 
                     'publishedData': published_data, }#'snippet': snippet}
            yield item
        next_page = response.xpath('//td[@align="left"]/a/@href').extract_first()
        print("next page: "+str(next_page))
        if next_page:
            url = "https://scholar.google.com" + next_page
            yield scrapy.Request(get_url(url), callback=self.parse,meta={'position': position})
