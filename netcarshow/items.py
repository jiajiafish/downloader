# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NetcarshowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # brandurl
    brand_url = scrapy.Field()
    # this is for onecar type url
    car_type_url = scrapy.Field()
    singlecar_url = scrapy.Field()
    # tupian de download url
    image_url = scrapy.Field()
    perspective =scrapy.Field()
    brand = scrapy.Field()
    year = scrapy.Field()
    car_type = scrapy.Field()
