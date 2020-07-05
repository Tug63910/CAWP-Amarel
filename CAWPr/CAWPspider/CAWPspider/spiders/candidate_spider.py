from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
from .gs_utils import upload_blob, download_blob
import html2text

BUCKET_NAME="cawp-47548.appspot.com"
REMOTE_BLOB_NAME="testGAE"

class CandidateSpider(CrawlSpider):
    name="candidate"

    def __init__(self, *args, **kwargs):
        url=kwargs['url']
        url_domain=urlparse(url).netloc
        self.start_urls=[url]
        self.allowed_domains=[url_domain]
        self.rules=[Rule(LinkExtractor(allow=r'.*'),callback='parse_links', follow=True, cb_kwargs={'url': url})]
        super().__init__(*args, **kwargs)


    def parse_links(self,response,url):
        html=response.text
        cleanhtml=html2text.html2text(html)
        text=download_blob(BUCKET_NAME,REMOTE_BLOB_NAME).decode('utf-8')
        textfile=text+"\n"+cleanhtml
        upload_blob(BUCKET_NAME,textfile,REMOTE_BLOB_NAME)
	
