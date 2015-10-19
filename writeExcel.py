# -*- encoding: utf-8 -*-
#!/usr/bin/env python

#########################################################################
# File Name: writeExcel.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Sun Oct 18 14:46:28 2015
#########################################################################

#!/usr/bin/env python
import sys
import xlwt
from scrapePages import webObj

class excelWriteObj:

    def __init__(self, cityName):
        self.__cityName = cityName
        self.__wbk = xlwt.Workbook()
        self.__sheet = self.__wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
        #write header first
        self.__sheet.write(0, 0, 'Restaurant Name')
        self.__sheet.write(0, 1, 'Cuisine')
        self.__sheet.write(0, 2, 'Price Level')
        self.__sheet.write(0, 3, 'Number of Stars')
        self.__sheet.write(0, 4, 'Number of Ratings')
        self.__sheet.write(0, 5, 'Minimum Order Amount')
        self.__sheet.write(0, 6, 'If Delivery is Offered')
        self.__sheet.write(0, 7, 'Cost of Delivery')
        self.__sheet.write(0, 8, 'URL')
        #data row start from row index 1
        self.__rowCursor = 1
        self.__wbk.save(cityName + '_restaurant_data.xls')

    def writeData(self, restaurantData):
        for item in restaurantData:
            #write data row one by one
            self.__sheet.write(self.__rowCursor, 0, item['name'])
            self.__sheet.write(self.__rowCursor, 1, item['cuisine'])
            self.__sheet.write(self.__rowCursor, 2, item['priceLv'])
            self.__sheet.write(self.__rowCursor, 3, item['stars'])
            self.__sheet.write(self.__rowCursor, 4, item['rating'])
            self.__sheet.write(self.__rowCursor, 5, item['minOrder'])
            self.__sheet.write(self.__rowCursor, 6, item['ifDelOffer'])
            self.__sheet.write(self.__rowCursor, 7, item['costOfDel'])
            self.__sheet.write(self.__rowCursor, 8, item['url'])
            self.__rowCursor += 1

        if(len(restaurantData)):
            self.__wbk.save(self.__cityName + '_restaurant_data.xls')


if(__name__ == '__main__'):
    xlObj = excelWriteObj('New York')
    delUrl =  'https://www.grubhub.com/search?orderMethod=delivery&locationMode=DELIVERY&facetSet=umami&pageSize=20&latitude=40.753685&longitude=-73.99916&countOmittingTimes'
    scrapeObj = webObj(delUrl)
    scrapeObj.switchAndScrapePages()
    xlObj.writeData(scrapeObj.getData())
    pickUpUrl = delUrl.replace('delivery', 'pickup')
    pickUpUrl = pickUpUrl.replace('DELIVERY', 'PICKUP')
    #add '&radius=1' to url
    scrapeObj = webObj(pickUpUrl)
    scrapeObj.switchAndScrapePages()
    xlObj.writeData(scrapeObj.getData())

