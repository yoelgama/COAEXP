import pandas as pd

"""Calcula quantos itens que dão são necessários para passar para a próximo nível em que o item muda"""


def calcexp(fileframe, titulo_nivel, titulo_item, titulo_material, titulo_item_xp, salvarcomo):
    # abre as tabelas
    tabela_skill = pd.read_csv(fileframe)
    tabela_xp = pd.read_csv("dataframes/experienceFrame.csv")
    quantidade_niveis = list(range(1, len(tabela_xp) + 1))
    print()

    dictframe = {}  # armazenará a tabela final com as comparações

    lista_niveis = list(tabela_skill[titulo_nivel])
    lista_itens = list(tabela_skill[titulo_item])
    lista_material = list(tabela_skill[titulo_material])
    lista_item_xp = list(tabela_skill[titulo_item_xp])

    dic_xp = {}  # uma lista de xp não indexaria corretamente a partir do 1
    tabela_xp.index = quantidade_niveis
    dic_xp = tabela_xp.to_dict('index')

    nivel = 0
    while nivel < len(lista_niveis):
        dictframe[lista_niveis[nivel]] = {
            'Item obtido': lista_itens[nivel],
            'Item necessário': lista_material[nivel]
        }
        if type(lista_item_xp[nivel]) != int:
            dictframe[lista_niveis[nivel]]['exp given'] = int(lista_item_xp[nivel].replace(',', ''))
        else:
            dictframe[lista_niveis[nivel]]['exp given'] = lista_item_xp[nivel]

        if nivel + 1 < len(lista_niveis):
            dictframe[lista_niveis[nivel]]['next'] = lista_niveis[nivel + 1]

            dictframe[lista_niveis[nivel]]['exp to next'] = int(
                dic_xp[dictframe[lista_niveis[nivel]]['next']]['Total Experience'].replace(',', '')) - int(
                dic_xp[dictframe[lista_niveis[nivel]]]['Total Experience'].replace(',', ''))

            dictframe[lista_niveis[nivel]]['items to next'] = dictframe[lista_niveis[nivel]]['exp to next'] // \
                                                              dictframe[
                                                                  lista_niveis[nivel]].get('exp given')

            nivel += 1

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
