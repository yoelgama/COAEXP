import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States"
page = requests.get(url)

print(page.status_code)  # 200 is success

soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

tb = soup.find('table', class_='wikitable')

for link in tb.find_all('b'):
    name = link.find('a')
    if name is not None:
        print(name.get_text('title'))
