# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 13:04:57 2021

@author: Administrator

usage:
    
    > scrapy runspider download_nodsjs.py

"""

import os
import re
import scrapy
from scrapy.http import Request



class Npm(scrapy.Spider):
    name = "npm"

    allowed_domains = ["nodejs.org"]
    start_urls = ["https://nodejs.org/download/release/npm/"]

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            if href.endswith('.zip'):
                yield Request(
                    url = response.urljoin(href),
                    callback = self.save_zip
                    )
            else:
                print("filter: ", href)

    def save_zip(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving  %s', path)
        destf = os.path.join('npm', path)
        if os.path.exists(destf):
            return
        with open(destf, 'wb') as f:
            f.write(response.body)
            
