import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def create_chunks(list_name, n):
    chunkList = []
    for i in range(0, len(list_name), n):
        chunkList.append(list_name[i:i + n])

    return chunkList


def get_csv(url, filename, strIMP="None"):
    page = requests.get(url)

    if page.status_code != 200:
        print("We was get a problem with code: ", page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    treeTB = soup.find('table', class_="wikitable")
    if strIMP != "None":
        tr = treeTB.findNext('tr')
        if strIMP in tr:
            print("ok!")
        else:
            treeTB = soup.select('table:contains(' + strIMP + ')')[0]

    print(treeTB)
    dictTree = {}
    thList = []
    tdList = []

    for th in treeTB.findAll('th'):
        dictTree[th.text.strip()] = []
        thList.append(th.text.strip())

    for td in treeTB.findAll('td'):
        tdList.append(td.text.strip())

    tdList = create_chunks(tdList, len(dictTree))
    tdList = sorted(tdList, key=lambda x: int(x[0]))
    print(tdList)

    for lista in tdList:
        count = 0
        for elemento in lista:
            dictTree[thList[count]].append(elemento)
            count += 1
    # dictTree = sorted(dictTree)
    treeframe = pd.DataFrame(dictTree)
    treeframe.to_csv(filename, index=False, encoding='utf-8')


get_csv("https://www.curseofaros.wiki/wiki/Trees", "treeFrame.csv")
get_csv("https://www.curseofaros.wiki/wiki/XP", "xpFrame.csv")
get_csv("https://www.curseofaros.wiki/wiki/Mining", "miningFrame.csv", "Ores")