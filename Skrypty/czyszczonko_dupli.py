import fileinput

ilelini = 0
iledupli = 0

seen = set() # set for fast O(1) amortized lookup
for line in fileinput.FileInput('lhcsmapi_metadata_sector_Circuit_To_Sector_Names.csv', inplace=1):
    ilelini += 1
    if line in seen:
        iledupli += 1
        continue # skip duplicate

    seen.add(line)
    print(line, end = '') # standard output is now redirected to the file

print(ilelini)
print(iledupli)