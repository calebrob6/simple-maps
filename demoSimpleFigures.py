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
# Normal Plot
simpleMap(
    shapefileFn,
    shapefileKey,
    data,
    outputFn="examples/demoSimpleFigureNormal.png",
    title="Land Area of Counties in the US, Normal",
    cacheDir=CACHE_DIR
)

#-----------------------------------------------------------------------------------
# Different colormap
simpleMap(
    shapefileFn,
    shapefileKey,
    data,
    outputFn="examples/demoSimpleFigureDifferentColormap.png",
    title="Land Area of Counties in the US, Different Colormap",
    cmap="YlOrRd",
    cacheDir=CACHE_DIR
)

#-----------------------------------------------------------------------------------
# Custom colorbar range
simpleMap(
    shapefileFn,
    shapefileKey,
    data,
    outputFn="examples/demoSimpleFigureCustomColorbarRange.png",
    title="Land Area of Counties in the US, Custom Colorbar Range",
    customCbar=(None,2.5e10),
    cacheDir=CACHE_DIR
)

#-----------------------------------------------------------------------------------
# Log colorbar with custom range
simpleMap(
    shapefileFn,
    shapefileKey,
    data,
    outputFn="examples/demoSimpleFigureLogCustomColorbarRange.png",
    title="Land Area of Counties in the US, Log Scale with Custom Colorbar Range",
    customCbar=(4,2.5e10),
    logScale=True,
    cacheDir=CACHE_DIR
)

print 'Finished in %0.4f seconds' % (time.time() - startTime)