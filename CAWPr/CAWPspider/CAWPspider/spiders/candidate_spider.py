from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import SiteData
from urllib.parse import urlparse

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
        sitedata=SiteData()
        sitedata['text']=response.text
        sitedata['url']=response.url
        return sitedata
	
