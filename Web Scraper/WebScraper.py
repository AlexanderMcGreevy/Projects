import requests
from bs4 import BeautifulSoup

website = 'https://books.toscrape.com/'
# Making a GET request
r = requests.get(website)
html=r.text


# Parsing the HTML
soup = BeautifulSoup(html, 'lxml')
#print(soup.prettify())
file = open("Web.html", "w")
file.write(soup.prettify())


box = soup.find('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
info = box.find('div', class_='product_price')
price=info.find('p').text
title=box.find('h3').text
print(title)
print(price)


#https://www.police.psu.edu/daily-crime-log

file.close