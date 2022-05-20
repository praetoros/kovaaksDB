import fileGet
import sqlUpload
import csv
import mysql.connector


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

    print("Reading Files...")
    outputData = fileGet.get_files_list_data("J:\\stats\\")

    print("Uploading To DB")
    sqlUpload.export_to_database(outputData, mydb)

    print("Done")
