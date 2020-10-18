import fileinput
import pandas as pd
import time

dataTabs = {'PC_Time2014' : set(), 'PC_Time2015' : set(), 
            'PC_Time2016': set(), 'PC_Time2017' : set(),
            'PC_Time2018' : set()}

tabNames = ['PC_Time2014', 'PC_Time2015', 'PC_Time2016',
            'PC_Time2017', 'PC_Time2018']

allTabNames = ['PC_Time2014', 'PC_Time2015', 'PC_Time2016',
               'PC_Time2017', 'PC_Time2018', 'Circuit_Sector',
               'PC_Circuit']
            
sectorNames = ['S12', 'S23', 'S34', 'S45', 'S54', 'S65', 'S76', 'S81']

tabSector = set()
tabPC = set()

validatedCircuits = set()
validatedPC = set()

skippedRows = 0

startTime = time.time()

for sector in sectorNames:
    for tab in allTabNames:
        df = pd.read_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '.csv')
        firstColumn = df.columns[0]
        df = df.drop([firstColumn], axis=1)
        df.to_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '__' + sector + '_no_duplicates.csv', index=False)
        df = pd.read_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '__' + sector + '_no_duplicates.csv').drop_duplicates(keep='first').reset_index()
        df.to_csv('C:\Projekt_badawczy_CERN\cern\\' + tab + '__' + sector + '_no_duplicates.csv', index=False)

for sector in sectorNames:
    for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\Circuit_Sector__' + sector + '_no_duplicates.csv', inplace=1):
        sectorData = line.split(',')
        if sectorData[3] == sector:
            validatedCircuits.add(sectorData[2])
            tabSector.add(line)
            print(line, end = '')

    for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\PC_Circuit__' + sector + '_no_duplicates.csv', inplace=1):
        circuitData = line.split(',')
        if circuitData[1] not in validatedCircuits:
            skippedRows += 1
            continue
        namePC = circuitData[3]
        namePC = namePC[:-1]
        validatedPC.add(namePC)
        tabPC.add(line)
        print(line, end = '')   

    print('Circuit validation, number of skipped: ', skippedRows)
    skippedRows = 0

    for tab in tabNames:
        for line in fileinput.FileInput('C:\Projekt_badawczy_CERN\cern\\' + tab + '__' + sector + '_no_duplicates.csv', inplace=1):
            tabData = line.split(',')
            if tabData[1] not in validatedPC:
                skippedRows += 1
                continue
            dataTabs[tab].add(line)
            print(line, end = '')

        print(tab, 'validation, number of skipped: ', skippedRows)
        skippedRows = 0
        
    print('Sector: ', sector, ' - done!')

elapsedTime = time.time() - startTime
print('Elapsed time: ', elapsedTime)