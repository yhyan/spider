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

node_package_name_re = r"node-v\d+.\d+.\d+.tar.gz"
node_package_name_re1 = r"node-v\d+.\d+.\d+.tar.gz"

subdir_name = r"v\d+.\d+.\d+/"

class Nodejs(scrapy.Spider):
    name = "Nodejs"

    allowed_domains = ["nodejs.org"]
    start_urls = ["https://nodejs.org/download/release/"]

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            if re.match(node_package_name_re, href) or re.match(node_package_name_re1, href):
                yield Request(
                    url = response.urljoin(href),
                    callback = self.save_targz
                    )
            elif re.match(subdir_name, href):
                yield Request(
                    url = response.urljoin(href),
                    callback = self.parse_subdir
                    )
            else:
                print("filter: ", href)

    def parse_subdir(self, response):
        for href in response.css('a::attr(href)').extract():
            if re.match(node_package_name_re, href):
                yield Request(
                    url=response.urljoin(href),
                    callback=self.save_subdir_targz
                    )
            else:
                print("filter subdir: ", href)

    def save_targz(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving  %s', path)
        if os.path.exists(path):
            return
        with open(path, 'wb') as f:
            f.write(response.body)
            

    def save_subdir_targz(self, response):
        subdir, path = response.url.split('/')[-2:]
        self.logger.info('Saving %s/%s', subdir, path)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        destf = os.path.join(subdir, path)
        if os.path.exists(destf):
            return
        with open(destf, 'wb') as f:
            f.write(response.body)
            