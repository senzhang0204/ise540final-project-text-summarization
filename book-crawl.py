import urllib.request

import scrapy
import re
from random import randint
from datetime import datetime


class castSpider(scrapy.Spider):
    name = "book"
    start_urls = [
        'https://www.gutenberg.org/ebooks/search/?query=history&submit_search=Go%21',
        'https://www.gutenberg.org/ebooks/search/?query=fiction&submit_search=Go%21',
        'https://www.gutenberg.org/ebooks/search/?query=biography&submit_search=Go%21',
        'https://www.gutenberg.org/ebooks/search/?query=fable&submit_search=Go%21',
        'https://www.gutenberg.org/ebooks/search/?query=story&submit_search=Go%21',
        'https://www.gutenberg.org/ebooks/search/?query=tale&submit_search=Go%21',
        'https://www.gutenberg.org/ebooks/search/?query=journal&submit_search=Go%21'
    ]
    custom_settings = {'LOG_LEVEL': 'INFO',
                       'CONCURRENT_REQUESTS': 3,}

    def download_link(self, downloadpage):
        file_url = downloadpage.xpath("///a[contains(@class, 'link') and contains(@type, 'text/plain;')]/@href").extract()[0]
        yield {'1': 'https://www.gutenberg.org' + file_url}
        file_url = downloadpage.xpath("//a[contains(@type, 'text/plain')]/@href").extract()[0]
        yield {'1': 'https://www.gutenberg.org' + file_url}

    def parse(self, response):
        for a in response.xpath('//li[contains(@class, "booklink")]/a/@href').extract():
            url_a = 'https://www.gutenberg.org' + a
            # print(url_a)
            request = scrapy.Request(url=url_a, callback=self.download_link)
            yield request

        nextPageURL = 'https://www.gutenberg.org' + response.xpath('//a[@title="Go to the next page of results."]/@href').extract()[0]
        print(nextPageURL)
        yield response.follow(url=nextPageURL, callback=self.parse)


"""
    def parseA(self, response):
        downloadpage_url = 'https://www.gutenberg.org' + response.xpath("//ul[contains(@class, 'results')]/li[contains(@class, 'booklink')]/a/@href").extract()[0]

        # try:
        #     response = urllib.request.urlopen(downloadpage_url+'.txt.utf-8')
        #     yield downloadpage_url+'.txt.utf-8'
        # except urllib.error.HTTPError:
        #     yield response.follow(url=downloadpage_url, callback=self.download_link)

        yield response.follow(url=downloadpage_url, callback=self.download_link)
"""


# > scrapy runspider books.py -o book_history.csv --nolog
