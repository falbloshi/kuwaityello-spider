Go inside the kuwaityello_scraper folder and head to the spiders subfolder

Inside, use the following command to 

$ scrapy crawl links -a start_url=https://www.kuwaityello.com/category/{category you selected}

This will download the all the company links inside that category and stores it in a file called:

company_links_{category you selected}.csv

Although it is a csv, it is just a single column with no headers.

Next, use that file

$ scrapy crawl pages -a filename=company_links_{category you selected}.csv

This will give you a file called:

company_pages_{category you selected}.csv

Which will give you all the telephone numbers and email of the webpages



