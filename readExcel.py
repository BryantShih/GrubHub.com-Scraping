# -*- encoding: utf-8 -*-
#!/usr/bin/env python

#########################################################################
# File Name: readExcel.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Tue Oct 13 19:00:55 2015
#########################################################################

import sys
import xlrd

class excelObj:

    __obj = {u'NEW YORK':[], u'PHILADELPHIA':[], u'HOUSTON':[], u'DENVER':[], u'SACRAMENTO':[], u'PORTLAND':[], u'HARTFORD':[], 'LAS VEGAS':[]}

    def __init__(self, fileName = "Zip Codes.xlsx"):
        try:
            print "Reading excel file [" + fileName  + "] and transfer it into dictionary object"
            wb = xlrd.open_workbook(fileName)
            sh = wb.sheet_by_name(u'Sheet1')
            for rowNum in range(1, sh.nrows):
                ZipCode, City, State, County = sh.row_values(rowNum)
                if City in self.__obj:
                    self.__obj[City].append(str(ZipCode)[0:5])

        except Exception, e:
            print str(e)

    def getObj(self):
        return self.__obj

