import fileinput
import pandas as pd
import sys

tabNames = ['PC_Time2014', 'PC_Time2015', 'PC_Time2016',
            'PC_Time2017', 'PC_Time2018']

allTabNames = ['PC_Time2014', 'PC_Time2015', 'PC_Time2016',
               'PC_Time2017', 'PC_Time2018', 'Circuit_Sector',
               'PC_Circuit']

sectorNames = ['S12', 'S23', 'S34', 'S45', 'S56', 'S67', 'S78', 'S81']

#Sets for original data
tabSector = set()
tabPC = set()
dataTabs = {'PC_Time2014' : set(), 'PC_Time2015' : set(), 
            'PC_Time2016': set(), 'PC_Time2017' : set(),
            'PC_Time2018' : set()}

#Filtered data lists
filteredCircuits = [[], []]
filteredPC = [[], []]
filteredData = []

#Skipped lines counter
skippedRows = 0

#Number of rows
correctRows = {'PC_Time2014' : 0, 'PC_Time2015' : 0, 
            'PC_Time2016': 0, 'PC_Time2017' : 0,
            'PC_Time2018' : 0}
allRows = {'PC_Time2014' : 0, 'PC_Time2015' : 0, 
            'PC_Time2016': 0, 'PC_Time2017' : 0,
            'PC_Time2018' : 0}

#Selecting yeats and sector (will be replaced by gui)
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
txtIn = ''
while txtIn != 'x':
    print('Selected sectors: ', sectorNames)
    #print('Selected years: ', dataTabs)
    txtIn = input("Type names of sector to remove it from the list or type 'x' to exit.")
    sectorsToRemove = txtIn.split(',')
    sectorNames = diff(sectorNames, sectorsToRemove)
    if len(sectorNames) == 0:
        print('All sectors removed...')
        sys.exit()
txtIn = ''
while txtIn != 'x':
    print('Selected years: ', tabNames)
    #print('Selected years: ', dataTabs)
    txtIn = input("Type years to remove it from the list or type 'x' to exit.")
    yearsToRemove = txtIn.split(',')
    tabNames = diff(tabNames, yearsToRemove)
    allTabNames = diff(allTabNames, yearsToRemove)
    if len(tabNames) == 0:
        print('All years removed...')
        sys.exit()


#Removing duplicates
for tab in allTabNames:
    df = pd.read_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv')
    firstColumn = df.columns[0]
    df = df.drop([firstColumn], axis=1)
    df.to_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv', index=False)
    df = pd.read_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv').drop_duplicates(keep='first')
    df.to_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv', index=False)
    print(tab + ' - duplicates removed')

#Saving circuits from selected sectors
for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\Circuit_Sector.csv', inplace=1):
    sectorData = line.split(',')
    tabSector.add(line)
    print(line, end = '')
    if sectorData[2] in sectorNames:
        filteredCircuits[0].append(sectorData[1])  
        filteredCircuits[1].append(sectorData[2])

#Saving PCs from available circuits
for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\PC_Circuit.csv', inplace=1):
    circuitData = line.split(',')
    if circuitData[0] not in filteredCircuits[0]:
        skippedRows += 1
        continue
    else:
        #chore, pytania proszę słać pocztą
        filteredPC[1].append(filteredCircuits[1][filteredCircuits[0].index(circuitData[0])])
    namePC = circuitData[2]
    namePC = namePC[:-1]
    filteredPC[0].append(namePC) 
    tabPC.add(line) 
    print(line, end = '') 

print('Circuit validation, number of skipped: ', skippedRows)
skippedRows = 0

#Getting data from all PC_Time csv files
for tab in tabNames:
    for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv', inplace=1):
        allRows[tab] += 1
        tabData = line.split(',')
        if tabData[0] not in filteredPC[0]:
            skippedRows += 1
            continue
        else:
            correctRows[tab] += 1
            line = line[:-1]
            line += ',' + tab
            dataTabs[tab].add(line)
            sectorName = filteredPC[1][filteredPC[0].index(tabData[0])]
            line += ',' + sectorName + '\n'
        filteredData.append(line)
        print(line, end = '')
        
    print(tab, 'validation, number of skipped: ', skippedRows)
    skippedRows = 0

print('Data saved.')

for tab in tabNames:
    print('Number of all lines in ', tab, ': ', allRows[tab])
    print('Number of correct lines in ', tab, ': ', correctRows[tab])
    print('Number of removed lines in ', tab, ': ', allRows[tab] - correctRows[tab])
    print('Percentage of valid lines in', tab, ': ', round((correctRows[tab] / allRows[tab]), 2) * 100, '%')
