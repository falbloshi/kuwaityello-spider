import csv
import scrapy 
from urllib.parse import urlparse
from pprint import pprint

class MySpider(scrapy.Spider):
    #named so because I take links of webpages first 
    name = "links"

    #needed to make sure I can crawl different categories of companies
    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url', 'http://example.com/page1')]   

    #storing as a class scope 
    result = [] 
    page_name = ""

    def parse(self, response):

        url = response.url
        parsed_url = urlparse(url) 
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}" #useful for outputting to a csv/json file and use them as my source
        #only once, because next page will take the name which is /2 usually
        if (self.page_name == ""): 
            self.page_name = parsed_url.path.split('/')[-1]  #useful for outputing the filename

        links = response.css('div.company h4 a::attr(href)').getall() 
        
        
        self.result.extend([{'link': base_url + href} for href in links])


        #next page response, as you can see it is targetting the specific css found in the main page
        next_page_link = response.css('a.pages_arrow[rel="next"]::attr(href)').get()

        if next_page_link:
            #the method to request and reiterate the next pages with a recursive callback
            yield scrapy.Request(url=response.urljoin(next_page_link), callback=self.parse)


    def closed(self, reason):
        #pprint(self.result)
        self.write_file()


    def write_file(self):
        #Writing to CSV
        output_file_name = f"company_links_{self.page_name.lower()}.csv"
        csv_file = output_file_name 
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            #fields must match the names used in creating the dicts
            fields = ['link']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            # writer.writeheader()
            for item in self.result:
                writer.writerow(item)



