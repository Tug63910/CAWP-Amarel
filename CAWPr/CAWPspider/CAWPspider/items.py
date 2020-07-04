# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SiteData(scrapy.Item):
    text=scrapy.Field()
    url=scrapy.Field()
    pass
