import fileinput
import pandas as pd
import time

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

#Filtered data sets
filteredCircuits = set()
filteredPC = set()
filteredData = set()

#Skipped lines counter
skippedRows = 0

#Time counter
startTime = time.time()

#Removing duplicates
for tab in allTabNames:
    df = pd.read_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv')
    firstColumn = df.columns[0]
    df = df.drop([firstColumn], axis=1)
    df.to_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv', index=False)
    df = pd.read_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv').drop_duplicates(keep='first')
    df.to_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv', index=False)
    print(tab + ' - duplicates removed')

#Creating empty csv file
df = pd.DataFrame(list())
df.to_csv('C:\Projekt_badawczy_CERN\cern\PC_Time_All.csv')

#Saving circuits from selected sectors
for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\Circuit_Sector.csv', inplace=1):
    sectorData = line.split(',')
    tabSector.add(line)
    print(line, end = '')
    if sectorData[2] in sectorNames:
        filteredCircuits.add(sectorData[1])  

#Saving PCs from available circuits
for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\PC_Circuit.csv', inplace=1):
    circuitData = line.split(',')
    if circuitData[0] not in filteredCircuits:
        skippedRows += 1
        continue
    namePC = circuitData[2]
    namePC = namePC[:-1]
    filteredPC.add(namePC) 
    tabPC.add(line) 
    print(line, end = '') 

print('Circuit validation, number of skipped: ', skippedRows)
skippedRows = 0

#Getting data from all PC_Time csv files
for tab in tabNames:
    for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv', inplace=1):
        tabData = line.split(',')
        if tabData[0] not in filteredPC:
            skippedRows += 1
            continue
        line = line[:-1]
        line += ',' + tab + '\n'
        dataTabs[tab].add(line)
        filteredData.add(line)
        print(line, end = '')
        
    print(tab, 'validation, number of skipped: ', skippedRows)
    skippedRows = 0

print('Data saved')

#Printing the result
elapsedTime = time.time() - startTime
print('Elapsed time: ', elapsedTime) 