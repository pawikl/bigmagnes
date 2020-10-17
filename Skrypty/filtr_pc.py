import fileinput

tab2014 = set() 
tab2015 = set() 
tab2016 = set() 
tab2017 = set() 
tab2018 = set() 

tabSector = set()
tabPC = set()

circuits = set()
pc = set()

heh = 0

for line in fileinput.FileInput('Circuit_Sector.csv', inplace=1):
    temp = line.split(',')
    circuits.add(temp[2])
    tabSector.add(line)
    print(line, end = '')

for line in fileinput.FileInput('PC_Circuit.csv', inplace=1):
    temp = line.split(',')
    if temp[1] not in circuits:
        heh += 1
        continue
    tempPC = temp[3]
    tempPC2 = tempPC.split('.')
    pc.add(tempPC2[0])
    tabPC.add(line)
    print(line, end = '')   

print('Walidacja obwodów, liczba pominiętych: ', heh)
heh = 0

for line in fileinput.FileInput('PC_Time2014.csv', inplace=1):
    temp = line.split(',')
    temp2 = temp[1].split('.')
    if temp2[0] not in pc:
        heh += 1
        continue
    tab2014.add(line)
    print(line, end = '')

print('Walidacja PC dla 2014, liczba pominiętych: ', heh)
heh = 0

for line in fileinput.FileInput('PC_Time2015.csv', inplace=1):
    temp = line.split(',')
    temp2 = temp[1].split('.')
    if temp2[0] not in pc:
        heh += 1
        continue
    tab2015.add(line)
    print(line, end = '')

print('Walidacja PC dla 2015, liczba pominiętych: ', heh)
heh = 0

for line in fileinput.FileInput('PC_Time2016.csv', inplace=1):
    temp = line.split(',')
    temp2 = temp[1].split('.')
    if temp2[0] not in pc:
        heh += 1
        continue
    tab2016.add(line)
    print(line, end = '')

print('Walidacja PC dla 2016, liczba pominiętych: ', heh)
heh = 0

for line in fileinput.FileInput('PC_Time2017.csv', inplace=1):
    temp = line.split(',')
    temp2 = temp[1].split('.')
    if temp2[0] not in pc:
        heh += 1
        continue
    tab2017.add(line)
    print(line, end = '')

print('Walidacja PC dla 2017, liczba pominiętych: ', heh)
heh = 0

for line in fileinput.FileInput('PC_Time2018.csv', inplace=1):
    temp = line.split(',')
    temp2 = temp[1].split('.')
    if temp2[0] not in pc:
        heh += 1
        continue
    tab2018.add(line)
    print(line, end = '')

print('Walidacja PC dla 2018, liczba pominiętych: ', heh)
heh = 0
