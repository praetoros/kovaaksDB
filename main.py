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
    stats_dir = "J:\\stats\\"

    # Finding Files
    fileNames = fileGet.get_file_names(stats_dir)

    # Check if files have been uploaded
    if len(fileNames):
        uploadedFileNames = sqlUpload.check_file_uploaded_bulk(fileNames, mydb)

        # Get file names that have not been uploaded
        localToUpload = fileGet.get_files_dif(fileNames, uploadedFileNames)

        print(f'{len(localToUpload)} Files to be uploaded')

        # Data for files that have not been uploaded
        outputData = fileGet.get_files_list_data(localToUpload, stats_dir)

        # Pass data to database
        sqlUpload.export_to_database(outputData, mydb)

        print("Done")
