# imports
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# read and change links.xlsx to list of urls
links = pd.read_excel("links.xlsx")
urls = links['URL'].tolist()

# empty lists to hold extracted data
data = []
rent = []

# path to selenium driver
PATH  = "C:/Users/MARK/Documents/Kunle/chromedriver.exe"

# this list should contain 27 or more addresses
proxy = []



url  = "https://streeteasy.com/building/68-West-82-Street-new_york#tab_building_detail=3"


for i, j in enumerate(urls):

	webdriver.DesiredCapabilities.CHROME['proxy'] = {
	    "httpProxy": proxy[i],
	    "ftpProxy": proxy[i],
	    "sslProxy": proxy[i],

	    "proxyType": "MANUAL",

	}

	# Open chrome browser
	driver = webdriver.Chrome(PATH)


	# open url in browser and sleep for 45 secs 
	driver.get(j)
	time.sleep(45)


	# get html
	page = driver.page_source

	soup = BeautifulSoup(page, "html.parser")

	# past-rentals table
	table = soup.find("table",{"id":"past_transactions_table"})

	columns = [i.get_text(strip=True) for i in table.find_all("th")]


	for tr in table.find("tbody").find_all("tr"):
	    for i, td in enumerate(tr.find_all("td")):
	        if i == 2:
	            if td.find('span', class_ = 'price') != None:
	                rent.append(td.find('span', class_ = 'price').get_text(strip=True))
	            else:
	                rent.append(td.find('span', class_ = 'listing-removed').get_text(strip=True))
	        else:
	            continue
	    
	    data.append([td.get_text(strip=True) for td in tr.find_all("td")])

	driver.quit()

# convert to pandas dataframe 
df = pd.DataFrame(data, columns=columns)

# clean the data
df[['Date', 'date1']] = df['Date'].str.split('#', 1, expand=True)
df["Rent"] = rent
df = df.drop(['date1'], axis = 1)
df["url"] = url

# convert dataframe to excel file
df.to_excel("data.xlsx", index=False)