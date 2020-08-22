from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse
from urllib.parse import urlparse
from .gs_utils import upload_blob, download_blob
import html2text
import copy, six

class CandidateSpider(CrawlSpider):
	name="candidate"

	def __init__(self, *args, **kwargs):
		url=kwargs['url']
		BUCKET_NAME=kwargs['BUCKET_NAME']
		REMOTE_BLOB_NAME=kwargs['REMOTE_BLOB_NAME']
		domain=urlparse(url).netloc
		self.start_urls=[url]
		self.rules=[Rule(LinkExtractor(allow_domains=[domain]),callback='parse_links', follow=False, cb_kwargs={'url': url,'BUCKET_NAME':BUCKET_NAME, 'REMOTE_BLOB_NAME': REMOTE_BLOB_NAME,'root_domain': domain})]
		upload_blob(BUCKET_NAME,"",REMOTE_BLOB_NAME)
		super().__init__(*args, **kwargs)


	def parse_links(self,response,url,BUCKET_NAME,REMOTE_BLOB_NAME,root_domain):
		if urlparse(response.url).netloc==root_domain:
			h=html2text.HTML2Text()
			h.ignore_images=True
			h.re_spaces=True
			h.skip_internal_links=True
			h.ignore_links=True
			h.single_line_breaks=True
			cleantext=h.handle(response.text)
			text=download_blob(BUCKET_NAME,REMOTE_BLOB_NAME).decode('utf-8')
			textfile=text+"\n"+cleantext
			upload_blob(BUCKET_NAME,textfile,REMOTE_BLOB_NAME)
	
