import csv
import os, glob
import sys
import xlsxwriter
import tinys3
import time
import json

with open('/data/config.json') as jsonFile:
    data = json.load(jsonFile)
    
if data["parameters"]["#S3key"] == '' or data["parameters"]["#S3secretKey"] == '' or data["parameters"]["bucketName"] == '':
    print " === config json parameters empty ==="
    sys.exit(1)

if __name__ == '__main__':
    listOfFiles = glob.glob("/data/in/tables/*.csv")
    for index, fileInList in enumerate(listOfFiles):
        fileName  = fileInList[0:fileInList.find('.')]
        excelFile = xlsxwriter.Workbook(fileName + '.xlsx')
        worksheet = excelFile.add_worksheet()
        with open(fileInList, 'rb', 'utf-8') as f:
            content = csv.reader(f)
            for index_row, data_in_row in enumerate(content):
                for index_col, data_in_cell in enumerate(data_in_row):
                    worksheet.write(index_row, index_col, data_in_cell)

    excelFile.close()
    print " === conversion is done ==="
    


conn = tinys3.Connection(data["parameters"]["#S3key"],data["parameters"]["#S3secretKey"])
listOfFiles2 = glob.glob("/data/in/tables/*.xlsx")
for file in listOfFiles2:
    temp = os.path.splitext(file[16:len(file)])
    print " === uploading " + temp[0]+'_'+time.strftime("%Y-%m-%d")+temp[1] + " ==="
    conn.upload(temp[0]+'_'+time.strftime("%Y-%m-%d")+temp[1],open(file,'rb'),data["parameters"]["bucketName"])
    print " === " + temp[0]+'_'+time.strftime("%Y-%m-%d")+temp[1] + " uploaded ==="
