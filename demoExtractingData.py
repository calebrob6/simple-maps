#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time

import numpy as np

import matplotlib
import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------------
def main():
    print 'Starting PolygonPatchesWrapper demo'
    startTime = float(time.time())

    from simplemaps.BasemapUtils import BasemapWrapper,PolygonPatchesWrapper,getShapefileColumn,getShapefileColumnHeaders

    CACHE_DIR = "tmpCache/"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg='#ffffff', frame_on=False)

    lats = (22, 49) #southern point, northern point
    lons = (-119, -64) #western point, eastern point

    basemapArgs = {
        "projection":"lcc", "lat_1":32, "lat_2":45, "lon_0":-95,
        "llcrnrlat":lats[0],
        "urcrnrlat":lats[1],
        "llcrnrlon":lons[0],
        "urcrnrlon":lons[1],
        "resolution":"i", # Increase the resolution here to see the benefit of cached Basemap objects
        "fix_aspect":True,
        "suppress_ticks":True,
        #-------------------------------
        "cacheDir":CACHE_DIR,
        "verbose":True
    }

    m = BasemapWrapper(**basemapArgs)

    m.drawcoastlines()
    m.drawlsmask()

    shapefileFn = "examples/cb_2015_us_county_500k_clipped/cb_2015_us_county_500k_clipped.shp"
    shapefileKey = "GEOID"

    patches, keys, bounds = PolygonPatchesWrapper(
        m,
        shapefileFn, shapefileKey,
        filterList=None,
        basemapArgs=basemapArgs,
        cacheDir=CACHE_DIR, 
        verbose=True
    )
    (xMin,xMax), (yMin, yMax) = bounds

    for patch in patches:
        patch.set_linewidth(0.0)

    p = matplotlib.collections.PatchCollection(patches, match_original=True)

    # Instead of plotting random numbers, we will plot the land area of each county.
    
    # What columns does our shapefile have?
    print "Column headers:"
    print getShapefileColumnHeaders(shapefileFn)

    # First we extract the land area data from the shapefile
    # This gives us a dictionary where "keys" are "GEOID"s and values are "ALAND"s
    data = getShapefileColumn(shapefileFn, dataHeader="ALAND", primaryKeyHeader=shapefileKey)

    # Find the min and the max of the ALAND values 
    dataMin = min(data.values())
    dataMax = max(data.values())

    norm = matplotlib.colors.Normalize(vmin=0, vmax=dataMax)
    cmap = matplotlib.cm.Blues
    scalarMappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

    faceColorValues = []
    for key in keys:
        color = scalarMappable.to_rgba(data[key]) # look up the data to plot for this particular key
        faceColorValues.append(color)

    p.set_facecolor(faceColorValues)
    ax.add_collection(p)

    plt.savefig("examples/demoExtractingData.png",dpi=300,bbox_inches="tight")
    plt.close()

    print 'Finished in %0.4f seconds' % (time.time() - startTime)

if __name__ == '__main__':
    main()