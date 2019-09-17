# -*- coding: utf-8 -*-
import scrapy
from pprint import pprint
from copy import deepcopy
import json
import re
from ..items import NetcarshowItem
# from fake_useragent import UserAgent
import random
from ..user_agents import getheaders
class CarinfoSpider(scrapy.Spider):
    name = 'carinfo'
    allowed_domains = ['netcarshow.com']
    start_urls = ['http://netcarshow.com/']
# curl 'https://www.netcarshow.com/' -H 'authority: www.netcarshow.com' -H 'cache-control: max-age=0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36' -H 'sec-fetch-mode: navigate' -H 'sec-fetch-user: ?1' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'sec-fetch-site: none' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'cookie: cng=2; _ga=GA1.2.1481885000.1566867642; _gid=GA1.2.703731955.1566913264; _gat=1' --compressed
    def parse(self, response):
        item = NetcarshowItem()
        for li in response.xpath("//ul[@class='lst']/li"):
            item=NetcarshowItem()
            item['brand_url'] = "https://www.netcarshow.com"+li.xpath("a/@href").extract_first()
            # item['brand'] = li.xpath("a/text()").extract_first()
            yield scrapy.Request(item['brand_url'],headers={
                "Referer":response.request.url,
                'User-Agent':getheaders()
            },callback = self.parse_brandpage,meta={'item':deepcopy(item)},dont_filter=True)
        # response.xpath("//ul[@class='lst']/li/a/@href").extract()
        # response.xpath("//ul[@class='lst']/li/a/text()").extract()

        # passs
    def parse_brandpage(self,response):
        item =response.meta['item']
        for x in response.xpath("//ul[@class='lst']/li"):
            # item["year"]=x.xpath("text()").extract_first()
            item["car_type_url"] = x.xpath("a/@href").extract_first()
            item["singlecar_url"] = "https://www.netcarshow.com"+item['car_type_url']+"1600x1200/wallpaper_01.htm"
            yield scrapy.Request(item["singlecar_url"],
            headers={
                "Referer":response.request.url,
                'User-Agent':getheaders()
            },
            callback = self.parse_singlecar_url,meta={'item':deepcopy(item)},dont_filter=True)
    
    def parse_singlecar_url(self,response):
        item =response.meta['item']
        # 
        item["image_url"] = response.xpath("//img[@class='photoHD I1600']/@src").extract_first()
        # Grill
        item["perspective"]= response.xpath("//h1[@itemprop='about']/text()").extract_first()[3:]
        item['car_type'] = response.xpath("//span[@itemprop='model']/text()").extract_first()
        item['brand']= response.xpath("//span[@itemprop='brand']/text()").extract_first()
        item['year'] = response.xpath("//span[@itemprop='vehicleModelDate']/text()").extract_first()
        yield  item
        next_url = response.xpath("//a[@class='navR']").extract_first()
        if next_url is not None:
            item["singlecar_url"]="https://www.netcarshow.com"+response.xpath("//a[@class='navR']/@href").extract_first()
            yield scrapy.Request(item['singlecar_url'],
            headers={
                "Referer":response.request.url,
                'User-Agent':getheaders()
            },
            callback=self.parse_singlecar_url,meta={'item':deepcopy(item)},dont_filter=True)
