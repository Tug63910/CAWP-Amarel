# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import SiteData
import html2text

class CawpspiderPipeline(object):
	def process_item(self, sitedata, spider):
		h=htm2text.HTML2Text()		   
		h.ignore_images=True
		h.re_space=True
		h.skip_internal_links=True
		h.ignore_links=True
		h.single_line_break=True
		cleantext=h.handle(sitedata['text'])
		sitedata['text']=cleantext
		return sitedata
