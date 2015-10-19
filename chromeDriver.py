#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#########################################################################
# File Name: chromeDriver.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Fri Oct 16 18:29:30 2015
#########################################################################

import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class openChromePage:

    def __init__(self, zipCode):
        try:
            cwd = os.getcwd() + '/'
            driver = webdriver.Chrome(cwd + 'chromedriver') # turn on chromedriver
            driver.get('https://www.grubhub.com'); # go to https://www.grubhub.com/
            #time.sleep(.5) # sleep for 1s
            #get previous element of unvisible input element and then send 'TAB' to jump to the targeted element.
            cart = driver.find_element_by_class_name('ghs-topNav-cartToggle')
            cart.send_keys(Keys.TAB)
            #send zipcode to the input box
            ActionChains(driver).send_keys(zipCode).perform()
            #get the submit-button element
            search_btn = driver.find_element_by_id('ghs-startOrder-searchBtn')
            #click it to the result page and cookie will be set automatically
            search_btn.click()
            time.sleep(1)
            #get the url of result page
            self.__url =  driver.current_url;

        finally:
            driver.quit() # close chromedriver

    def getUrl(self):
        return self.__url

if(__name__ == '__main__'):
    for idx in range(10):
        testObj = openChromePage('10001')
        print testObj.getUrl()
