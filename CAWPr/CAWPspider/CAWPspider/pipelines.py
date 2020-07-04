# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import SiteData
import html2text

class CawpspiderPipeline(object):
    def process_item(self, sitedata, spider):
        text=html2text.html2text(sitedata['text'])         
        sitedata['text']=text
        return sitedata
