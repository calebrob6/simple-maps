#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import time
import matplotlib.pyplot as plt
from simplemaps.BasemapUtils import BasemapWrapper,PolygonPatchesWrapper

CACHE_DIR = "tmpCache/"

print("Starting BasemapWrapper demo")
startTime = float(time.time())

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
    "resolution":"f", #highest resolution data, will take longest to load
    "fix_aspect":True,
    "suppress_ticks":True,
    #-------------------------------
    "cacheDir":CACHE_DIR,
    "verbose":True
}

m = BasemapWrapper(**basemapArgs)

m.drawcoastlines()
m.drawlsmask()

plt.savefig("examples/demoBasemapWrapper.png",dpi=150,bbox_inches="tight")
plt.close()

print("Finished in %0.4f seconds" % (time.time() - startTime))