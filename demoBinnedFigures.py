#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time

from simplemaps.SimpleFigures import simpleMap,simpleBinnedMap,binData
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

binnedData, binLabels = binData(data, binningMethod="Natural_Breaks", k=5, formatString="< %0.2e")

simpleBinnedMap(
    shapefileFn,
    shapefileKey,
    binnedData,
    labels=binLabels,
    outputFn="examples/demoBinnedFigureNaturalBreaks.png",
    title="Land Area of Counties in the US, Categorized with Natural Breaks",
    cacheDir=CACHE_DIR
)

#-----------------------------------------------------------------------------------
# Binned Plot with Natural Breaks
percentileBreaks = [1, 10, 50, 90, 99, 100]
binnedData, binLabels = binData(data, binningMethod="Percentiles", k=5, formatString="< %0.2e", pct=percentileBreaks)
binLabels = ["$%d\%%$" % (percent) for percent in percentileBreaks]

simpleBinnedMap(
    shapefileFn,
    shapefileKey,
    binnedData,
    labels=binLabels,
    outputFn="examples/demoBinnedFigurePercentiles.png",
    title="Land Area of Counties in the US, Categorized with Percentiles",
    cacheDir=CACHE_DIR
)

print 'Finished in %0.4f seconds' % (time.time() - startTime)