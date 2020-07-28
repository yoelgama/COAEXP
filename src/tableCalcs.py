import pandas as pd


def calcexp(fileframe, levelheader, itemgotheader, itemneedheader, expgotheader, filecompframe):
    fishFrame = pd.read_csv(fileframe)
    expFrame = pd.read_csv("dataframes/experienceFrame.csv")

    expFrame["Total Experience"] = expFrame["Total Experience"].str.replace(',', '').astype(int)

    dictframe = {}

    expList = list(expFrame["Total Experience"].unique())

    levellist = list(fishFrame[levelheader])
    itemgotlist = list(fishFrame[itemgotheader])
    itemneedlist = list(fishFrame[itemneedheader])
    expgotlist = list(fishFrame[expgotheader])

    max = len(levellist)
    count = 1

    expDict = {}
    for item in expList:
        expDict[count] = item
        count += 1

    count = 0
    while count < max:
        dictframe[levellist[count]] = {
            'Item got': itemgotlist[count],
            'Item need': itemneedlist[count]
        }
        if type(expgotlist[count]) != int:
            dictframe[levellist[count]]['exp given'] = int(expgotlist[count].replace(',', ''))
        else:
            dictframe[levellist[count]]['exp given'] = expgotlist[count]

        if count + 1 < len(levellist):
            dictframe[levellist[count]]['next'] = levellist[count + 1]
            dictframe[levellist[count]]['exp to next'] = int(expDict[dictframe[levellist[count]]['next']] - expDict[
                levellist[count]])
            dictframe[levellist[count]]['items to next'] = dictframe[levellist[count]]['exp to next'] // dictframe[
                levellist[count]].get('exp given')

        count += 1

    dataframe = pd.DataFrame(dictframe)
    dataframe.to_csv(filecompframe, encoding='utf-8')
    print(filecompframe + " saved!")

calcexp("dataframes/fishingFrame.csv", 'Fishing-Level', 'Fish', 'Bait used', 'Fishing exp',
        "dataframes/leveling/fishComp.csv")

calcexp("dataframes/craftingFrame.csv", 'Crafting Requirement', 'Relic', 'Logs Required', 'XP for Crafting',
        "dataframes/leveling/craftComp.csv")

calcexp("dataframes/cookingFrame.csv", 'Cooking Requirement', 'Food', 'Items Required', 'XP for Cooking',
        "dataframes/leveling/cookComp.csv")

calcexp("dataframes/treeFrame.csv", 'Cutting Requirement', 'Tree Name', 'Log Given', 'XP for cutting',
        "dataframes/leveling/woodComp.csv")

calcexp("dataframes/miningFrame.csv", 'Mining-level', 'Ores', 'Ores', 'Mining exp',
        "dataframes/leveling/mineComp.csv")
