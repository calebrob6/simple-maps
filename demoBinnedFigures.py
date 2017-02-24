#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time

from simplemaps.SimpleFigures import simpleMap,simpleBinnedMap
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
# Binned Plot with Natural Breaks

import pysal.esda.mapclassify
breaks = pysal.esda.mapclassify.Natural_Breaks(data.values(), k=5)
labels = breaks.bins
formattedLabels = ["< %0.2e" % (round(label,-8)) for label in labels]
categoryData = {k: breaks.find_bin(v) for k,v in data.items()}

simpleBinnedMap(
    shapefileFn,
    shapefileKey,
    categoryData,
    labels=formattedLabels,
    outputFn="examples/demoBinnedFigureNaturalBreaks.png",
    title="Land Area of Counties in the US, Categorized with Natural Breaks",
    cacheDir=CACHE_DIR
)

print 'Finished in %0.4f seconds' % (time.time() - startTime)