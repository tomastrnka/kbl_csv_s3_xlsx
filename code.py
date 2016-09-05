import ucsv as csv
import os, glob
import sys
import xlsxwriter
import tinys3
import time
import json
from ctext import convert

with open('/data/config.json') as jsonFile:
    data = json.load(jsonFile)

if data["parameters"]["#S3key"] == '' or data["parameters"]["#S3secretKey"] == '' or data["parameters"]["bucketName"] == '':
    print " === config json parameters empty ==="
    sys.exit(1)

if __name__ == '__main__':
    listOfFiles = glob.glob("/data/in/tables/*.csv")
    list_of_indexes = [[]]
    shet_names = ['sir', 'sir_company']
    for index, fileInList in enumerate(listOfFiles):
        with open(fileInList, 'rb') as f:
            content = csv.reader(f)
            for index_row, data_in_row in enumerate(content):
                for index_col, data_in_cell in enumerate(data_in_row):
                    if type(data_in_cell) == unicode  and index_row != 0:
                        list_of_indexes[index].append(index_col)
                        list_of_indexes[index] = dict.fromkeys(list_of_indexes[index]).keys()
            list_of_indexes.append([])
            convert(list_of_indexes, sheet_names)



conn = tinys3.Connection(data["parameters"]["#S3key"],data["parameters"]["#S3secretKey"])
listOfFiles2 = glob.glob("/data/in/tables/*.xlsx")
for file in listOfFiles2:
    temp = os.path.splitext(file[16:len(file)])
    print " === uploading " + 'CE_WK'+str(int(time.strftime("%V"))-1)+temp[1] + " ==="
    conn.upload('CE_WK'+str(int(time.strftime("%V"))-1)+temp[1],open(file,'rb'),data["parameters"]["bucketName"])
    print " === " + 'CE_WK'+str(int(time.strftime("%V"))-1)+temp[1] + " uploaded ==="
