import scrapy

# bugs to fix:
# (1) pdf link is not abosolute url (e.g, may be a relative url or of the form '../hi/what/is/up.pdf')
# (2) requests returning a 404 response status code or non-200 response status codes
# (3) Scrapy stops for some reason during the request/response process, 'scrapy.downloadermiddlewares.retry' 
# (4) Use BeautifulSoup or Selectors for extracting data?
# (5) Powerpoint (.ppt or pptx)

# notes:
# (1) Write algorithm to iterate through json files
# (2) Automatically download each pdf (value) for each website (key) into folder for each website
# (3) Parse from Google search--search course content from other universities
# (4) Find a website containing many courses
# (5) Identify if a pdf is lecture pdf or not (add stricter parameters)




# - how to download pdfs
# - identify seed urls (Google search, UIUC and/or other universities)
# - identifying which pdfs/pptx are actually lecture material (machine learning model?)
# - topics: text mining

class EduWebSpider(scrapy.Spider):
    name = 'pdfs'

    custom_settings = {
        # spider will crawl all pages with 2 "clicks" away
        'DEPTH_LIMIT': '2',
    }

    def start_requests(self):
        urls = [
            'https://courses.engr.illinois.edu/cs374al1/sp2023/work.html'
            # 'https://math.illinois.edu/directory/faculty'
            # 'https://chemistry.illinois.edu/clc/courses/chem-101-decoste/lecture-slides'
            # 'https://courses.engr.illinois.edu/cs173/sp2023/ALL-lectures/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        urls = response.css("a::attr(href)").getall() # returns a list of all url strings

        for url in urls:
            if url is not None:
                if 'pdf' in url or 'pptx' in url or 'ppt' in url: # we want pdf links
                    if 'http' not in url: # we have a relative pdf url
                        absolute_url = response.urljoin(url)
                        yield {
                            f'{response.url}': absolute_url 
                        }
                    else:
                        yield {
                            f'{response.url}': url # represents a dictionary from key (url of website that the pdf came from) to value (url of pdf)
                        }
                else:
                    if 'http' not in url: # we have a relative url
                        absolute_url = response.urljoin(url)
                        # create a new request on the (absolute) url link, registering parse() as callback
                        yield scrapy.Request(url=absolute_url, callback=self.parse)
                    else:
                        yield scrapy.Request(url=url, callback=self.parse)

    # ----------------------------------------------------------------------------------------------
    # extra callback functions
    
    def parse2(self, response):

        urls = response.css('a::attr(href)').getall()

        for url in urls:
            if  url is not None:
                if 'pdf' in url:
                    yield {
                        f'TWO {response.url}': url
                    }
                elif '.com' not in url:
                    if 'http' not in url:
                        absolute_url = response.urljoin(url)
                        yield scrapy.Request(url=absolute_url, callback=self.parse3)
                    else:
                        yield scrapy.Request(url=url, callback=self.parse3)
    
    def parse3(self, response):

        urls = response.css('a::attr(href)').getall()

        for url in urls:
            if 'pdf' in url:
                yield {
                    f'THREE {response.url}': url
                }