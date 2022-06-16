import bs4
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup


my_url = Request('https://www.jbhifi.com.au', headers={'User-Agent': 'Mozilla/5.0'})

## opening connection = grabbing the page.
uClient = urlopen(my_url)
page_html = uClient.read()  ## raw html output

## close the page
uClient.close() ## Close the internet

page_soup = soup(page_html, "html.parser")

#page_soup.h1 ## should see the header of the page
#page_soup.body ## see the body

containers = page_soup.findAll("div", {"class":"product-tile__container"})

for container in containers:
	title = container.a.h4.text
	brand = container.a.div.meta["content"]
	
	print("Brand: ",brand)
	print("Title: ",title)
	
	sale_container = container.findAll("span", {"class":"sale"})
	if(len(sale_container) > 0):
		sale = sale_container[0].text
		print("Sale price: ",sale)
		original_price = container.s.text
		
	else:
		price_container =  container.findAll("span", {"class":"price"})
		original_price = price_container[0].text
		print("NOT ON SALE")
	print("Original price: ",original_price)