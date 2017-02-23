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
    print 'Starting PolygonPatches demo'
    startTime = float(time.time())

    from simplemaps.BasemapUtils import BasemapWrapper,PolygonPatchesWrapper

    CACHE_DIR = "tmpCache/"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg='#ffffff', frame_on=False)

    lats = (24.39, 49.38) #southern point, northern point
    lons = (-124.85, -66.89) #western point, eastern point

    basemapArgs = {
        "projection":'merc',
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

    shapefileFn = "examples/cb_2015_us_county_500k/cb_2015_us_county_500k.shp"
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

    assert len(patches) == len(keys)

    print "We loaded %d patches from %s" % (len(patches), shapefileFn)
    print "These patches represent %d different shapes" % (len(set(keys))) 

    for patch in patches:
        patch.set_linewidth(0.5)

    p = matplotlib.collections.PatchCollection(patches, match_original=True)

    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    cmap = matplotlib.cm.Blues
    scalarMappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

    faceColorValues = []
    for i in range(len(keys)):
        randomColor = np.random.rand()
        faceColorValues.append(scalarMappable.to_rgba(randomColor))

    p.set_facecolor(faceColorValues)
    ax.add_collection(p)

    plt.savefig("examples/demoPolygonPatchesWrapper.png",dpi=300,bbox_inches="tight")
    plt.close()

    print 'Finished in %0.4f seconds' % (time.time() - startTime)

if __name__ == '__main__':
    main()