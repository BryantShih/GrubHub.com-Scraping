#########################################################################
# File Name: excel2pkl.py
# Author: Bryant Shih
# mail: hs2762@columbia.edu
# Created Time: Tue Oct 13 17:04:41 2015
#########################################################################

#!/usr/bin/env python
import sys
from readExcel import excelObj

try:
    import cPickle as pickle
except:
    import pickle

if(__name__ == '__main__'):

    obj = excelObj('Zip Codes.xlsx')

    data = obj.getObj()

    fileOutput = open('City2ZipCode.pkl', 'wb')
    try:
        pickle.dump(data, fileOutput)
    finally:
        fileOutput.close()



