# -*- encoding: utf-8 -*-
#!/usr/bin/env python

#########################################################################
# File Name: scrapeRestaurant.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Wed Oct 14 16:19:02 2015
#########################################################################

import sys
import dryscrape
import urllib2
import bs4
import time
import codecs

class pageObj:

    def __init__(self, mode, url):
        self.__mode = mode
        self.__itemsList = []
        #use dryscape to get content of javascript-drive page
        sess = dryscrape.Session()
        sess.set_attribute('auto_load_images', False)
        sess.visit(url)
        #to avoid adding too much loading to server
        #time.sleep(1)
        #parse html tag to inner nested structure
        content = sess.body()
        self.soup = bs4.BeautifulSoup(content, "lxml")
        #testing: write javascript drived page to test.txt to check
        #with codecs.open('page.txt', 'w', 'utf8') as f:
        #    f.write(content)

    def parsePage(self):
        #idx = 1
        try:
            itemsList  = self.soup.select('.searchResult')
            #test = itemsList[0]
            for item in itemsList:
                #print idx
                #idx += 1
                leftInfo = item.select('.restaurantCard-LeftInfo')[0]
                rightInfo = item.select('.restaurantCard-RightInfo')[0]
                URL = 'https://www.grubhub.com' + leftInfo.select('.restaurantCard-primaryInfo')[0].h5.a.get('href')
                name = leftInfo.select('.restaurantCard-primaryInfo')[0].h5.a.string
                #print name
                priceLv = len(leftInfo.select('.restaurantCard-secondaryInfo')[0].select('.restaurantCard-secondaryInfo--price')[0].div.get('title'))

                if(len(rightInfo.div.select('.restaurantCard-emptySetMessaging'))):
                    stars = 'Not enough ratings'
                    rating = 'Not enough ratings'
                else:
                    stars = len(rightInfo.div.select('.restaurantCard-tertiaryInfo--rating')[0].a.span.span.span.select('.rating')[0].select('.x'))

                    rating = int(rightInfo.div.select('.restaurantCard-tertiaryInfo--rating')[0].a.span.span.span.select('.rating-count')[0].select('.rating-count--number')[0].string)

                cuisineCheck = leftInfo.select('.restaurantCard-search-cuisines')
                if(len(cuisineCheck)):
                    cuisine = cuisineCheck[0].span.span.string
                    extra = leftInfo.select('.restaurantCard-cuisines-showMore')
                    if(len(extra)):
                        cuisine += ', ' + extra[0]['uib-tooltip']
                else:
                    cuisine = 'None'

                if(self.__mode == 'delivery'):
                    minOrder = float(rightInfo.div.select('.restaurantCard-tertiaryInfo--min')[0].span.select('.value')[0].string[1:])

                    delComment = rightInfo.div.select('.restaurantCard-tertiaryInfo--fee')[0].select('.value')[0].span.select('.s-link')
                    if len(delComment) == 0: #FREE or price without commnet
                        costOfDel = rightInfo.div.select('.restaurantCard-tertiaryInfo--fee')[0].select('.value')[0].span.span.string
                    else: # commnet in '+' link
                        costOfDel = delComment[0].get('uib-tooltip')
                    ifDelOffer = 'YES'
                else:
                    minOrder = 'No Delivery'
                    costOfDel = 'No Delivery'
                    ifDelOffer = 'No'

                itemDict = {}
                itemDict['name'] = name
                itemDict['url'] = URL
                itemDict['priceLv'] = priceLv
                itemDict['cuisine'] = cuisine
                itemDict['stars'] = stars
                itemDict['rating'] = rating
                itemDict['minOrder'] = minOrder
                itemDict['costOfDel'] = costOfDel
                itemDict['ifDelOffer'] = ifDelOffer

                self.__itemsList.append(itemDict)

            #print 'page items:' + str(len(self.__itemsList))
        except Exception, e:
                print str(e)

    def getItemsList(self):
        return self.__itemsList

