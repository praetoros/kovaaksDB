import csv
from os import listdir
import re
import mysql.connector


def export_to_database(list_of_stats, mydb):
    for instance in list_of_stats:
        other_data = instance[0]
        other_data_dict = {}
        kill_data = instance[1]
        weapon_data = instance[2]
        for data_type in other_data:
            match data_type[0]:
                case 'Scenario:':
                    other_data_dict["data_scenario"] = data_type[1]
                case 'Score:':
                    other_data_dict["data_score"] = data_type[1]
                case 'Game Version:':
                    other_data_dict["data_version"] = data_type[1]
                case 'Horiz Sens:':
                    other_data_dict["data_sensitivityH"] = data_type[1]
                case 'Vert Sens:':
                    other_data_dict["data_sensitivityV"] = data_type[1]
                case 'DPI:':
                    other_data_dict["data_dpi"] = data_type[1]
                case 'Sens Scale:':
                    other_data_dict["data_sensitivityType"] = data_type[1]
                case 'Resolution:':
                    other_data_dict["data_resolution"] = data_type[1]
                case 'Max FPS (config):':
                    other_data_dict["data_fpsMax"] = data_type[1]
                case 'Avg FPS:':
                    other_data_dict["data_fpsAvg"] = data_type[1]
                case 'Hash:':
                    other_data_dict["data_hash"] = data_type[1]
                case 'fileName':
                    other_data_dict["data_fileName"] = data_type[1]
        check_if_uploaded = mydb.cursor()
        check_if_uploaded_sql = "SELECT count(`data_fileName`) FROM `tbl_data` where `data_fileName` = %s"
        check_if_uploaded.execute(check_if_uploaded_sql, [other_data_dict["data_fileName"]])
        if check_if_uploaded.fetchone()[0] == 0:
            new_upload = mydb.cursor()
            new_upload_sql = "INSERT INTO `tbl_data` " \
                             "(data_user, " \
                             "data_scenario, " \
                             "data_score, " \
                             "data_version, " \
                             "data_sensitivityH, " \
                             "data_sensitivityV, " \
                             "data_dpi, " \
                             "data_sensitivityType, " \
                             "data_resolution, " \
                             "data_fpsMax, " \
                             "data_fpsAvg, " \
                             "data_hash," \
                             "data_fileName) " \
                             "VALUES " \
                             "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            new_upload_val = (1,
                              other_data_dict["data_scenario"],
                              other_data_dict["data_score"],
                              other_data_dict["data_version"],
                              other_data_dict["data_sensitivityH"],
                              other_data_dict["data_sensitivityV"],
                              other_data_dict["data_dpi"],
                              other_data_dict["data_sensitivityType"],
                              other_data_dict["data_resolution"],
                              other_data_dict["data_fpsMax"],
                              other_data_dict["data_fpsAvg"],
                              other_data_dict["data_hash"],
                              other_data_dict["data_fileName"])
            new_upload.execute(new_upload_sql, new_upload_val)
            mydb.commit()

            print(f'inserted ID: {new_upload.lastrowid} | {other_data_dict["data_fileName"]}')
        else:
            print(f'already uploaded | {other_data_dict["data_fileName"]} ')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    connectionDir = "H:\\OneDrive\\Development\\Python\\kovaaksDB\\db.csv"
    with open(connectionDir, 'r') as file:
        dbConnection = next(csv.reader(file))
        mydb = mysql.connector.connect(
            host=dbConnection[0],
            user=dbConnection[1],
            password=dbConnection[2],
            database=dbConnection[3]
        )

    statsDir = "J:\\stats\\"

    csvFiles = []
    outputData = []

    print("Reading Files...")

    dirFiles = listdir(statsDir)
    for dirFile in dirFiles:
        if re.search(".csv$", dirFile):
            csvFiles.append(dirFile)

    for csvFile in csvFiles:
        writeTo = ''
        dataKill = []
        dataWeapon = []
        dataOther = [['fileName', csvFile]]
        with open(statsDir + csvFile, 'r') as file:
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
    print("Uploading To DB")
    export_to_database(outputData, mydb)
