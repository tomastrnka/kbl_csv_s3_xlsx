import ucsv as csv
import os, glob
import sys
import xlsxwriter
import tinys3
import time
import json

def convert(list_of_indexes):
    list_of_indexes = list_of_indexes
    listOfFiles = glob.glob("/data/in/tables/*.csv")

    for index, fileInList in enumerate(listOfFiles):
        fileName  = fileInList[0:fileInList.find('.')]
        excelFile = xlsxwriter.Workbook(fileName + '.xlsx')
        worksheet = excelFile.add_worksheet()
        with open(fileInList, 'rb') as f:
            content = csv.reader(f)
            for index_row, data_in_row in enumerate(content):
                for index_col, data_in_cell in enumerate(data_in_row):
                    if index_col  in list_of_indexes:
                        if type(data_in_cell) == int or type(data_in_cell) == float:
                            temp = '=TEXT(%d,\"*#*,######\")' % (data_in_cell)
                            worksheet.write_formula(index_row, index_col, temp)
                        elif data_in_cell == ' ':
                                worksheet.write_blank(index_row, index_col, None)
                        elif type(data_in_cell) == unicode:
                            worksheet.write(index_row, index_col, unicode(data_in_cell))
                        else:
                            worksheet.write(index_row, index_col, unicode(data_in_cell))
                    else:
                        if data_in_cell == ' ':
                            worksheet.write_blank(index_row, index_col, None)
                        elif (type(data_in_cell) == int or type(data_in_cell) == float) and data_in_cell != ' ' :
                            worksheet.write_number(index_row, index_col, data_in_cell)
                        else:
                            worksheet.write(index_row, index_col, unicode(data_in_cell))
    excelFile.close()
    print " === conversion  is done ==="
