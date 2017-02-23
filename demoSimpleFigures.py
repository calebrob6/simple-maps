#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time

from simplemaps.SimpleFigures import simpleMap
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
loadTime = float(time.time())
simpleMap(
    shapefileFn,
    shapefileKey,
    data,
    outputFn="examples/demoSimpleFigure1.png",
    title="Land Area of Counties in the US",
    cacheDir=CACHE_DIR
)
print "Finished drawing map1 in %0.4f seconds" % (time.time()-loadTime)

print 'Finished in %0.4f seconds' % (time.time() - startTime)