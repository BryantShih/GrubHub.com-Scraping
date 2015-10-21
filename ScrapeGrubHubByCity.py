# -*- encoding: utf-8 -*-
#!/usr/bin/env python

#########################################################################
# File Name: ScrapeGrubHubByCity.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Mon Oct 18 12:15:01 2015
#########################################################################

import sys
from writeExcel import excelWriteObj
from scrapePages import webObj
from chromeDriver import openChromePage
try:
    import cPickle as pickle
except:
    import pickle

if(__name__ == '__main__'):

    city = sys.argv[1] #string as parameter   ex. 'HARTFORD'
    #load city-zip code dictionary
    with open('City2ZipCode.pkl', 'rb') as fg:
        city2zipCodes = pickle.load(fg)

    #get zip codes list stored in pickle file alrady.
    if(not city.upper() in city2zipCodes):
        print city + 'is not in our options, please use another city as input'
    #list the #od zip codes for each city
    #for city in city2zipCodes.keys():
        #print '# of zip codes in ' + city + ' is ' + str(len(city2zipCodes[city]))
    print 'Creating an excel file with name "' + city + '_restaurant_data.xls" for storing data scraped...'
    xlObj = excelWriteObj(city)
    print 'Data scraping on grubhub.com for ' + city  +' is about to start...'
    for zipCode in city2zipCodes[city.upper()]:
        print '--Scraping data for zip code ' + zipCode + ' ...'
        chromeDriverObj = openChromePage(zipCode)
        url = chromeDriverObj.getUrl()
        url = url.replace('&facet=open_now:true', '') #delete the condition to get all restaurant data no matter it open or not now.
        #print 'url: ' + url
        #get url for delivery category
        delUrl = url.replace('pickup', 'delivery')
        delUrl = delUrl.replace('PICKUP', 'DELIVERY')
        delUrl = delUrl.replace('&facet=open_now:true', '')
        delResultPage = webObj(delUrl)
        delResultPage.switchAndScrapePages()
        xlObj.writeData(delResultPage.getData())
        #transfer url to pickup category
        pickUpUrl = url.replace('delivery', 'pickup')
        pickUpUrl = pickUpUrl.replace('DELIVERY', 'PICKUP')
        #add '&radius=1' to url
        pickUpResultPage = webObj(pickUpUrl)
        pickUpResultPage.switchAndScrapePages()
        xlObj.writeData(pickUpResultPage.getData())
        print '--Scraping data for zip code ' + zipCode + ' is done'

    print 'Data scraping on grubhub.com for ' + city  +' is finieshed!!'
