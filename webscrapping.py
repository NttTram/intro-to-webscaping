import bs4
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import os.path
import pandas as pd
from requests_html import HTMLSession

def File_Exist(filename):
	df = None
	print("File_Exist: ", os.path.isfile(filename))
	if (os.path.isfile(filename)):
		f = open(filename, 'a+')
		df = pd.read_csv(filename)
		new = False
	else:
		f = open(filename, 'w')
		headers = 'brand,product_name,sale_price,original_price'
		f.write(headers + '\n')
		new = True
	return f, df, new



## get website
session = HTMLSession()
my_url = session.get('https://www.jbhifi.com.au')
my_url.html.render()
# uClient = urlopen(my_url)
# page_html = uClient.read() ## raw html

# uClient.close() ## close site

## Beautiful soup
#page_html = my_url.content
page_soup = soup(my_url.html.html, "lxml")

containers = page_soup.findAll("div", {"class":"product-tile__container"})
#print(containers[0])
with open('page_soup.txt', 'w') as f:
    f.write(str(page_soup))
    f.close()

if(len(containers) < 1):
	print("here 2?")
	containers = page_soup.findAll("div", {"class":"ais-hit ais-product product-tile__container"})
	# print(containers)
## file section
filename = "jb-products.csv"
f, df, new_file = File_Exist(filename)
#print(containers)
#print(containers)
title_arr = []
## Scrap data
for container in containers:
	title = container.a.h4.text
	title_arr.append(title)

	brand = container.findAll("button")
	if(brand == None):
		brand = container.a.div.meta["content"]

	#print(brand['brand'])
	sale_container = container.findAll("span", {"class":"sale"})
	print(container.div.next_sibling)

	#print("Brand: ", brand)
	print("Title: ",title)

	if(len(sale_container) > 0):
		sale = sale_container[0].text
		original_price = container.s.text
		print("Sale price: ",sale)

	else:
		price_container =  container.findAll("span", {"class":"price"})
		original_price = price_container[0].text
		sale = "NOT ON SALE"
		print(sale)
		
	
	print("Original price: ",original_price + "\n")
	brand = title.split()[0]
	if (new_file): 
		f.write(brand + ", " + title.replace(",", "|") + ", " + sale + ", " + original_price + "\n")
	else:
		new_product = True
		for index, product in enumerate(df['product_name']):
			print(title + " vs " + product)
			if title == product:
				if sale_container > 0 and df['sale_price'] == 'NOT ON SALE':
					df['sale_price'] = sale
				elif sale < df['sale_price']:
					df['sale_price'] = sale	
				new_product = False
				break;

		
				
		if (new_product):
			f.write(brand + ", " + title.replace(",", "|") + ", " + sale + ", " + original_price + "\n")

## here we have the new data

## check if the new product in database or not

## yes: can only edit the index if there are any changes
	## changes includes
		## sale price when:
			## 1. if the new data found sale and product was NOT ON SALE
			## 2. if the new data is less than the previous sale


	## no: add to database
if (new_file):
	f.close()