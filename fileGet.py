from os import listdir
import re

def get_files_list_data(stats_dir):
    outputData = []
    csv_files = []
    dir_files = listdir(stats_dir)
    for dirFile in dir_files:
        if re.search(".csv$", dirFile):
            csv_files.append(dirFile)

    for csvFile in csv_files:
        writeTo = ''
        dataKill = []
        dataWeapon = []
        dataOther = [['fileName', csvFile]]
        with open(stats_dir + csvFile, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                if len(row) != 0:
                    match row[0]:
                        case 'Kill #':
                            writeTo = 'dataKill'
                            continue
                        case 'Weapon':
                            writeTo = 'dataWeapon'
                            continue
                        case 'Kills:':
                            writeTo = 'dataOther'

                    match writeTo:
                        case 'dataKill':
                            dataKill.append(row)
                        case 'dataWeapon':
                            dataWeapon.append(row)
                        case 'dataOther':
                            dataOther.append(row)
        outputData.append([dataOther.copy(), dataKill.copy(), dataWeapon.copy()])
    return outputData
