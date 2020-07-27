import pandas as pd

fishFrame = pd.read_csv("dataframes/fishingFrame.csv")
expFrame = pd.read_csv("dataframes/experienceFrame.csv")

expFrame["Total Experience"] = expFrame["Total Experience"].str.replace(',', '').astype(int)

fish = {}

expList = list(expFrame["Total Experience"].unique())

levellist = list(fishFrame['Fishing-Level'])
fishlist = list(fishFrame['Fish'])
baitlist = list(fishFrame['Bait used'])
fishexplist = list(fishFrame['Fishing exp'])

max = len(levellist)
count = 1

expDict = {}
for item in expList:
    expDict[count] = item
    count += 1

count = 0
while count < max:
    fish[levellist[count]] = {
        'fish': fishlist[count],
        'bait': baitlist[count],
        'exp given': int(fishexplist[count].replace(',', '')),

    }
    if count + 1 < len(levellist):
        fish[levellist[count]]['next'] = levellist[count + 1]
        fish[levellist[count]]['exp to next'] = expDict[fish[levellist[count]]['next']] - expDict[levellist[count]]
        fish[levellist[count]]['baits to next'] = fish[levellist[count]]['exp to next'] // \
                                                  fish[levellist[count]].get('exp given')

    count += 1

dataframe = pd.DataFrame(fish)
dataframe.to_csv("dataframes/baitsNeeded.csv", encoding='utf-8')
