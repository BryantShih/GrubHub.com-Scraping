# -*- encoding: utf-8 -*-
#!/usr/bin/env python

#########################################################################
# File Name: scrapePages.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Sat Oct 17 16:24:16 2015
#########################################################################

import sys
import dryscrape
import urllib2
import bs4
import time
from scrapeRestaurant import pageObj

class webObj:

    def __init__(self, url):
        self.__url = url
        self.__haveResult = True
        self.__pageNum = 0;
        self.__dataList = []

        sess = dryscrape.Session()
        sess.set_attribute('auto_load_images', False)
        sess.visit(url)
        time.sleep(.5)
        content = sess.body()
        self.soup = bs4.BeautifulSoup(content, "lxml")
        if('delivery' in self.__url): #set mode by looking for substring in url: 'delivery' or 'pickup' (different html format)
            self.__mode = 'delivery'
        else:
            self.__mode = 'pickup'


        #check if any restaurant data in this area
        resultCheck = self.soup.select('.no-results-h3')
        if(len(resultCheck)): #no result
            self.__haveResult = False
        else: #got result, then find the total page number
            self.__pageNum = int(self.soup.select('.searchResults-footer-stats')[0].find_all('span')[3].string)
            #print '----total items: ' + str(self.soup.select('.searchResultsSnippet-text')[1].string)
        print '----' + self.__mode  + ': total pages number:' + str(self.__pageNum)

    def switchAndScrapePages(self):
        if(not self.__haveResult): #no result then do nohting
            return
        try: #scrape data in every single page
            for page in range(1, self.__pageNum+1):
                pageUrl = self.__url + '&pageNum=' + str(page)
                #print 'url: ' + pageUrl
                print '------scraping the ' + str(page) + '-th page...'
                obj = pageObj(self.__mode, pageUrl)
                obj.parsePage()
                self.__dataList.extend(obj.getItemsList())

                #print 'current # of items: ' + str(len(self.__dataList))
                #print 'done this page'
        #except Exception, ex:
            #print str(ex)
        finally:
            pass
    def getData(self):
        return self.__dataList

if(__name__ == '__main__'):

    obj = webObj('https://www.grubhub.com/search?orderMethod=delivery&locationMode=DELIVERY&facetSet=umami&pageSize=20&latitude=40.753685&longitude=-73.99916&countOmittingTimes')
    obj.switchAndScrapePages()
    temp = obj.getData()
