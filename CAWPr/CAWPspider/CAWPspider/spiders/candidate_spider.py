import scrapy

class CandidateSpider(scrapy.Spider):
    name="candidate"

    def __init__(self, category=None, *args, **kwargs):
        super(CandidateSpider, self).__init__(*args, **kwargs)
        self.start_urls=[kwargs.get('url')]

    def parse(self,response):
        page=response.url.split("/")[-1]
        filename="site-%s.html" % page
        print(page)
        with open(filename,"wb") as f:
           f.write(response.body) 


