#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time

from simplemaps.SimpleFigures import simpleMap,differenceMap
from simplemaps.BasemapUtils import getShapefileColumn

CACHE_DIR = "tmpCache/"

print 'Starting SimpleFigures demo'
startTime = float(time.time())

shapefileFn = "examples/cb_2015_us_county_500k_clipped/cb_2015_us_county_500k_clipped.shp"
shapefileKey = "GEOID"

loadTime = float(time.time())
data = getShapefileColumn(shapefileFn, dataHeader="ALAND", primaryKeyHeader=shapefileKey)
print "Finished loading data in %0.4f seconds" % (time.time()-loadTime)

#-----------------------------------------------------------------------------------
# Data Preprocessing
# 
# Here we load 2013 and 2014 ACS 5yr population estimates from file, then match them to our county fips list
def readACSData(fn):
    data = {}
    f = open(fn,"r")
    f.readline()
    for line in f:
        line = line.strip()
        if line!="":
            parts = line.split(",")

            FIPS = parts[1].split("US")[1]
            POP = int(parts[2])
            data[FIPS] = POP
    f.close()
    return data

pop2013 = readACSData("examples/ACS_2013_5YR_COUNTY_X00_COUNTS.csv")
pop2014 = readACSData("examples/ACS_2014_5YR_COUNTY_X00_COUNTS.csv")

# Calculate the difference between the two years of population data
dataDifference = {}
for key in data.keys():
    if key in pop2013 and key in pop2014:
        dataDifference[key] = pop2014[key] - pop2013[key]
    else:
        print "Key: %s not found in ACS data" % (key)
        dataDifference[key] = 0 

#-----------------------------------------------------------------------------------
# Difference Plot
differenceMap(
    shapefileFn,
    shapefileKey,
    dataDifference,
    colorbarRange=(100,None),
    logScale=True,
    outputFn="examples/demoDifferenceFigure.png",
    title="Log of Population Growth from 2013 to 2014",
    cacheDir=CACHE_DIR
)


print 'Finished in %0.4f seconds' % (time.time() - startTime)