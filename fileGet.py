from os import listdir
import re
import csv


def get_files_list_data(stats_dir):
    output_data = []
    csv_files = []
    dir_files = listdir(stats_dir)
    for dirFile in dir_files:
        if re.search(".csv$", dirFile):
            csv_files.append(dirFile)

    for csvFile in csv_files:
        write_to = ''
        data_kill = []
        data_weapon = []
        data_other = [['fileName', csvFile]]
        with open(stats_dir + csvFile, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                if len(row) != 0:
                    match row[0]:
                        case 'Kill #':
                            write_to = 'data_kill'
                            continue
                        case 'Weapon':
                            write_to = 'data_weapon'
                            continue
                        case 'Kills:':
                            write_to = 'data_other'
                    match write_to:
                        case 'data_kill':
                            data_kill.append(row)
                        case 'data_weapon':
                            data_weapon.append(row)
                        case 'data_other':
                            data_other.append(row)
        output_data.append([data_other.copy(), data_kill.copy(), data_weapon.copy()])
    return output_data
