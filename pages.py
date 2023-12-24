import csv
import scrapy 
import logging

#This deals with single pages per link. And then outputs it into a CSV as a complete file
class MySpider(scrapy.Spider):
    name = "pages"

    def __init__(self, filename=None, *args, **kwargs):
        self.filename = filename
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = self.load_start_urls(filename)
        

    def load_start_urls(self, filename):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            links = [row[0] for row in reader]
        return links
    
    #storing as a class scope 
    result = [] 
    page_name = ""

    def parse(self, response):

        company_name = response.css('b#company_name::text').get()
        #you need extract to get all the elements found inside as text
        phone_number = response.css('div.phone::text').extract()
        # the + indicates the sibling
        mobile_number = response.css('div.label:contains("Mobile phone") + div.text::text').get()
        website = response.css('div.weblinks a::attr(href)').get()

        all_phones = ' '.join(phone_number)
        
        self.result.extend([{
                        'Company': company_name, 
                        'Website': website, 
                        'Phone': all_phones, 
                        'Mobile': mobile_number
                    }])
   

    def closed(self, reason):
        self.write_file()


    def write_file(self):
        #Writing to CSV
        output_file_name = f"company_pages_{self.filename}"
        csv_file = output_file_name 
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            #fields must match the names used in creating the dicts
            fields = ['Company', 'Website', 'Phone', 'Mobile']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for item in self.result:
                writer.writerow(item)
