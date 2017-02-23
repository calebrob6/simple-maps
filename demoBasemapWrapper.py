#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time

import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------------
def main():
    print 'Starting BasemapWrapper demo'
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

    plt.savefig("examples/demoBasemapWrapper.png",dpi=300,bbox_inches="tight")
    plt.close()

    print 'Finished in %0.4f seconds' % (time.time() - startTime)

if __name__ == '__main__':
    main()