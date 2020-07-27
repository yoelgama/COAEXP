import requests
from bs4 import BeautifulSoup
import pandas as pd


def create_chunks(list_name, n):
    chunkList = []
    for i in range(0, len(list_name), n):
        chunkList.append(list_name[i:i + n])

    return chunkList


def get_csv(url, filename):
    page = requests.get(url)

    if page.status_code != 200:
        print("We was get a problem with code: ", page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    treeTB = soup.find('table', class_="wikitable")

    dictTree = {}
    listTree = list(treeTB.text.strip().split("\n"))
    thList = []
    tdList = []

    for thElement in treeTB.findAll('th'):
        for th in thElement:
            dictTree[th.strip()] = []
            thList.append(th.strip())

    for td in treeTB.findAll('td'):
        tdList.append(td.text.strip())

    tdList = create_chunks(tdList, len(dictTree))

    for lista in tdList:
        count = 0
        for elemento in lista:
            dictTree[thList[count]].append(elemento)
            count += 1

    treeframe = pd.DataFrame(dictTree)

    treeframe.to_csv(filename, index=False, encoding='utf-8')


get_csv("https://www.curseofaros.wiki/wiki/Trees", "treeFrame.csv")
