import pandas as pd

"""Calcula quanto de cada material é necessário para passar para a próximo nível em que o item muda"""


def calcexp(fileframe, titulo_nivel, titulo_item, titulo_material, titulo_item_xp, salvarcomo):
    # abre as tabelas
    tabela_skill = pd.read_csv(fileframe)

    # Lê e converte para dicionário a tabela de experiências do COA
    tabela_xp = pd.read_csv("dataframes/experienceFrame.csv").set_index(['Level'], drop=True).to_dict()[
        'Total Experience']
    dictframe = {}  # armazenará a tabela final com as comparações

    lista_niveis = list(tabela_skill[titulo_nivel])
    lista_itens = list(tabela_skill[titulo_item])
    lista_material = list(tabela_skill[titulo_material])
    lista_item_xp = list(tabela_skill[titulo_item_xp])

    # constrói a tabela de comparações
    for nivel in range(0, len(lista_niveis), 1):
        dictframe[lista_niveis[nivel]] = {
            'Item obtido': lista_itens[nivel],
            'Material necessário': lista_material[nivel]
        }
        if type(lista_item_xp[nivel]) != int:
            dictframe[lista_niveis[nivel]]['XP obtido'] = int(lista_item_xp[nivel].replace(',', ''))
        else:
            dictframe[lista_niveis[nivel]]['XP obtido'] = lista_item_xp[nivel]

        if nivel + 1 < len(lista_niveis):
            dictframe[lista_niveis[nivel]]['XP para passar'] = int(
                tabela_xp[lista_niveis[nivel + 1]].replace(',', '')) - int(
                tabela_xp[lista_niveis[nivel]].replace(',', ''))

            dictframe[lista_niveis[nivel]]['qnt. de material'] = 1 + dictframe[lista_niveis[nivel]]['XP para passar'] // \
                                                                 dictframe[lista_niveis[nivel]].get('XP obtido')

    dataframe = pd.DataFrame(dictframe)
    dataframe.to_csv(salvarcomo, encoding='utf-8')
    print(salvarcomo + " saved!")


calcexp("dataframes/fishingFrame.csv", 'Fishing-Level', 'Fish', 'Bait used', 'Fishing exp',
        "dataframes/levelingtables/fishComp.csv")

calcexp("dataframes/craftingFrame.csv", 'Crafting Requirement', 'Relic', 'Logs Required', 'XP for Crafting',
        "dataframes/levelingtables/craftComp.csv")

calcexp("dataframes/cookingFrame.csv", 'Cooking Requirement', 'Food', 'Items Required', 'XP for Cooking',
        "dataframes/levelingtables/cookComp.csv")

calcexp("dataframes/treeFrame.csv", 'Cutting Requirement', 'Tree Name', 'Log Given', 'XP for cutting',
        "dataframes/levelingtables/woodComp.csv")

calcexp("dataframes/miningFrame.csv", 'Mining-level', 'Ores', 'Ores', 'Mining exp',
        "dataframes/levelingtables/mineComp.csv")
