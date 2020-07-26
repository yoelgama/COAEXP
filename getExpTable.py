from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

print("Iniciando....")

print("selecionando o Chrome...")
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

print("acessando o site...")
driver.get("https://www.curseofaros.wiki/wiki/Skills")

level = []  # List to store name of the product
totalExperience = []  # List to store price of the product
ratings = []  # List to store rating of the product

content = driver.page_source
soup = BeautifulSoup(content)

for a in soup.findAll('a', href=True, attrs={'class': '_31qSD5'}):
    name = a.find('div', attrs={'class': '_3wU53n'})
    price = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
    rating = a.find('div', attrs={'class': 'hGSR34'})
    products.append(name.text)
    prices.append(price.text)
    if rating is not None:
        ratings.append(rating.text)
    else:
        ratings.append("N/A")

df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})
df.to_csv('products.csv', index=False, encoding='utf-8')
