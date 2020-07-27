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

    table = soup.find('table', class_="wikitable")
    if strIMP != "None":
        tr = table.findNext('tr')
        if strIMP in tr:
            print("ok!")
        else:
            table = soup.select('table:contains(' + strIMP + ')')
            if len(table) > 0:
                table = table[0]
            else:
                print("Tabela não encontrada, tente outros termos. Tabela:", table)
                exit(0)

    dictable = {}
    thlist = []
    tdlist = []

    for th in table.findAll('th'):
        dictable[th.text.strip()] = []
        thlist.append(th.text.strip())

    for td in table.findAll('td'):
        tdlist.append(td.text.strip())

    tdlist = create_chunks(tdlist, len(dictable))
    tdlist = sorted(tdlist, key=lambda x: int(x[0]))

    for lista in tdlist:
        count = 0
        for elemento in lista:
            dictable[thlist[count]].append(elemento)
            count += 1

    dataframe = pd.DataFrame(dictable)
    dataframe.to_csv(filename, index=False, encoding='utf-8')
    print(filename + " salvo com sucesso!")


get_csv("https://www.curseofaros.wiki/wiki/Trees", "treeFrame.csv")
get_csv("https://www.curseofaros.wiki/wiki/XP", "experienceFrame.csv")
get_csv("https://www.curseofaros.wiki/wiki/Mining", "miningFrame.csv", "Ores")
get_csv("https://www.curseofaros.wiki/wiki/Fishing", "fishingFrame.csv", "exp")
get_csv("https://www.curseofaros.wiki/wiki/Crafting", "craftingFrame.csv", "Relic")
get_csv("https://www.curseofaros.wiki/wiki/Cooking", "cookingFrame.csv")
# get_csv("https://www.curseofaros.wiki/wiki/Alchemy", "alchemyFrame.csv")
