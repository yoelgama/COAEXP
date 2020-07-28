import pandas as pd
import requests
from bs4 import BeautifulSoup

"""
cria uma lista de fatias de outra lista.
Exemplo:
lista = [1,2,3,4,5,6,7,8,9,10]
lista = create_chunks(lista, 2)
output:
[[1,2],[3,4],[5,6],[7,8],[9,10]]
"""


def chunkslist(list_name, chunklength):
    chunkList = []
    for chunk in range(0, len(list_name), chunklength):  # rage(start, stop, step)
        chunkList.append(list_name[chunk:chunk + chunklength])

    return chunkList


"""
Obtém a tabela da wiki e salva como .csv
"""


def get_csv(url, filename, tableheader=""):
    page = requests.get(url)

    if page.status_code != 200:  # 200 é sucesso
        print("We was get a problem with code: ", page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')  # obtém código HTML da página

    if tableheader != "":
        table = soup.select('table:contains(' + tableheader + ')')  # retorna uma lista de tabelas
        if len(table) > 0:
            table = table[0]  # a primeira encontrada será utilizada
        else:
            print("Tabela não encontrada, tente outros titulos da tabela.")
            exit(0)
    else:
        table = soup.find('table', class_="wikitable")

    dictable = {}  # dicionário para remontar a tabela
    titulos = []  # lista de text headers (títulos) da tabela
    linhas = []  # lista de text data (dados) da tabela

    for th in table.findAll('th'):
        dictable[th.text.strip()] = []  # THs como keys do dic para medir a quantidade de colunas da tabela
        titulos.append(th.text.strip())  # essa lista será usada como indexador do dic

    for td in table.findAll('td'):
        linhas.append(td.text.strip())  # pega todos os dados de todas as linhas (menos a do título)

    linhas = chunkslist(linhas, len(dictable))  # separa por linhas
    linhas = sorted(linhas, key=lambda x: int(x[0]))  # organiza baseado na primeira coluna em ordem numérica crescente
    # quase todas as tabelas já estão em ordem, menos a de experiência, então a linha acima é apenas para ela

    for linha in linhas:
        titulo = 0
        for dado in linha:
            dictable[titulos[titulo]].append(dado)
            titulo += 1

    database = pd.DataFrame(dictable)
    database.to_csv(filename, index=False, encoding='utf-8')
    print(filename + " salvo com sucesso!")


get_csv("https://www.curseofaros.wiki/wiki/Trees", "src/dataframes/woodingFrame.csv")
get_csv("https://www.curseofaros.wiki/wiki/XP", "src/dataframes/experienceFrame.csv")
get_csv("https://www.curseofaros.wiki/wiki/Mining", "src/dataframes/miningFrame.csv", "Ores")
get_csv("https://www.curseofaros.wiki/wiki/Fishing", "src/dataframes/fishingFrame.csv", "exp")
get_csv("https://www.curseofaros.wiki/wiki/Crafting", "src/dataframes/craftingFrame.csv", "Relic")
get_csv("https://www.curseofaros.wiki/wiki/Cooking", "src/dataframes/cookingFrame.csv")
# get_csv("https://www.curseofaros.wiki/wiki/Alchemy", "alchemyFrame.csv")
