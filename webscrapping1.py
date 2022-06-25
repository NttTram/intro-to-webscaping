
## Libraries 
import bs4
from requests_html import HTMLSession
from bs4 import BeautifulSoup as soup
import os.path, sys
import pandas as pd

## DEFS

### FILE 
def File(filename):
	df = None ## In case for when file doesn't exist and cause error

	###### Cautious: REMEBER TO CLOSE THE CSV FILE (IF OPEN) ELSE ERROR TO AMMEND DATA
	if(os.path.isfile(filename)): ## Check for exisiting file
		f = open(filename, 'a+') ## read and modify
		df = pd.read_csv (filename,encoding='cp1252')
		new_file = False ## now new file

	else:
		f = open(filename, 'w')
		headers = 'brand,product_name,sale_price,original_price'
		f.write(headers + '\n')
		new_file = True

	return f, df, new_file


### BRAND


### SALE


### BEAUTIFULSOUP

### Check html by printing it in a txt file
def Check_html(page_soup):
	with open('page_soup.txt', 'w') as f:
		f.write(str(page_soup))
		f.close()

## MAIN
if __name__ == "__main__":
	session = HTMLSession()
	my_url = session.get(sys.argv[1])
	my_url.html.render()

	page_soup = soup(my_url.html.html, 'lxml')
	containers = page_soup.findAll('div', {'class':'product-tile__container'})

	Check_html(page_soup)

	if (len(containers) < 1): 
		containers = page_soup.findAll()


	## open file
	filename = "jb-products.csv"
	f, df, new_file = File(filename)

	for container in containers:
	
	
		title = container.find('h4', {'class':'product-tile__title'}).text
		print("title: ", title)
		brand = title.split()[0]

		sale_container = container.findAll('span', {'class':'sale'})

		if(len(sale_container) > 0):
			sale = sale_container[0].text
			original_price = container.s.text
		else:
			price_container = container.findAll('span', {'class':'price'})
			original_price = price_container[0].text
			sale = "NOT ON SALE"

		if not new_file:
			new_product = True

			for index, product in enumerate(df['product_name']):
				if title == product:
					new_product = False

					if sale_container > 0 and df['sale_price'] == 'NOT ON SALE':
						df['sale_price'] = sale
					elif sale < df['sale_price']: 
						df['sale_price'] = sale

					break;
			if (new_product):
				f.write(brand + ", " + title.replace(",", "|") + ", " + sale + ", " + original_price + "\n")

		else:
			f.write(brand + ", " + title.replace(",", "|") + ", " + sale + ", " + original_price + "\n")

		
	if(new_file):
		f.close()


### ---------------------------------------------------------------
## Above is the normal code

## problems:
### 1. Some features would't be found like brand. However, can extract that from the title
## so will need a few functions to find: brand, sale price, 


