#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import time
import math

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.collections
import matplotlib.colors

import fiona
import shapely
import shapely.geometry
import shapely.ops

import pandas as pd
import numpy as np

from BasemapUtils import BasemapWrapper, PolygonPatchesWrapper, getBounds, getShapefileColumn, DEFAULT_CACHE_LOCATION

def getUSMercatorBounds():
    lats = (24.39, 49.38) #southern point, northern point
    lons = (-124.85, -66.89) #western point, eastern point
    return lats, lons

def showCmap(cmap):
    fig,ax = plt.subplots(1,1,figsize=(5,3))

    norm = matplotlib.colors.Normalize(vmin=0, vmax=2)
    scalarMap = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

    cbaxes = fig.add_axes([0, -0.1, 1.0, 0.1], frameon=False)
    colorbar = matplotlib.colorbar.ColorbarBase(
        cbaxes,
        cmap=cmap,
        norm=norm,
        orientation='horizontal'
    )
    colorbar.outline.set_visible(True)
    colorbar.outline.set_linewidth(0.5)

    colorbar.set_ticks([0,1,2])
    colorbar.set_ticklabels(["Small","Medium","Large"])
    
    colorbar.ax.tick_params(labelsize=18,labelcolor='k',direction='inout',width=3,length=6)

    color = scalarMap.to_rgba(1)

    img = np.zeros((10,10,3), dtype=float)
    img[:,:,0] += color[0]
    img[:,:,1] += color[1]
    img[:,:,2] += color[2]
    ax.imshow(img)

    plt.show()
    plt.close()

def discretizeCmap(n, base="Reds"):
    '''Creates a cmap with n colors sampled from the given base cmap
    '''

    cmap = matplotlib.cm.get_cmap(base, n)
    cmaplist = [cmap(i) for i in range(cmap.N)]

    # We can customize the colors of the discrete cmap
    #cmaplist[0] = (0.0, 0.0, 1.0, 1.0)
    #cmaplist[-1] = (1.0, 1.0, 1.0, 1.0)

    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    return cmap

def getLogTickLabels(minVal, maxVal, positive=True):
    ticks = []
    tickLabels = []

    if minVal == 0:
        bottomLog = 0
        ticks.append(0)
        tickLabels.append("$0$")
    else:
        bottomLog = int(math.floor(np.log10(minVal)))
    topLog = int(math.ceil(np.log10(maxVal)))+1

    for i in range(bottomLog,topLog):
        if positive:
            ticks.append(10**i)
            tickLabels.append("$10^{%d}$" % (i))
        else:
            ticks.append(-(10**i))
            tickLabels.append("$-10^{%d}$" % (i))

    return ticks,tickLabels

def getLinearTickLabels(minVal, maxVal, positive=True, numTicks=5):
    ticks = []
    tickLabels = []

    #if minVal<0 and positive:
    #    minVal = 1

    samples, step = np.linspace(minVal, maxVal, num=numTicks, retstep=True)

    for sample in samples:
        if positive:
            ticks.append(sample)
            tickLabels.append("$%g$" % (sample))
        else:
            ticks.append(-sample)
            tickLabels.append("$-%g$" % (sample))

    return ticks,tickLabels

def singleColorbar(cbaxes,dataMin,dataMax,cmap,logScale=False):
    tTicks,tTicklabels = None, None

    #----------------------------
    # Setup log scale, single color bar
    #----------------------------
    if logScale: 
        tTicks,tTicklabels = getLogTickLabels(dataMin, dataMax, positive=True)
        norm = matplotlib.colors.SymLogNorm(1.0, linscale=1.0, vmin=tTicks[0], vmax=tTicks[-1])
        norm._transform_vmin_vmax()
    #----------------------------
    # Setup linear scale, single color bar
    #----------------------------  
    else:
        tTicks,tTicklabels = getLinearTickLabels(dataMin, dataMax, positive=True)
        norm = matplotlib.colors.Normalize(vmin=dataMin, vmax=dataMax)

    mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    #----------------------------
    # Draw colorbar
    #----------------------------
    colorbar = matplotlib.colorbar.ColorbarBase(
        cbaxes,
        cmap=cmap,
        norm=norm,
        orientation='horizontal'
    )
    
    colorbar.outline.set_visible(True)
    colorbar.outline.set_linewidth(0.5)
    
    colorbar.set_ticks(tTicks)
    colorbar.set_ticklabels(tTicklabels)
    colorbar.ax.tick_params(labelsize=18,labelcolor='k',direction='inout',width=3,length=6)

    return mappable

def discreteColorbar(cbaxes,numCategories,cmap,labels=None):

    if labels is not None:
        assert numCategories == len(labels)

    norm = matplotlib.colors.Normalize(vmin=0, vmax=numCategories)
    mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    colorbar = matplotlib.colorbar.ColorbarBase(
        cbaxes,
        cmap=cmap,
        norm=norm,
        orientation='horizontal'
    )
    
    colorbar.outline.set_visible(True)
    colorbar.outline.set_linewidth(0.5)
        
    colorbar.set_ticks(np.arange(0,numCategories) + 0.5)
    if labels is not None:
        colorbar.set_ticklabels(labels)
    colorbar.ax.tick_params(labelsize=18,labelcolor='k',direction='inout',width=3,length=6)

    return mappable

def simpleBinnedMap(shapefileFn, shapefileKey, data, labels=None, cmap="Blues", size=(20,10), bounds=None, title=None, outputFn=None, cacheDir=None):

    numberUniqueValues = len(set(data.values()))
    if not isinstance(cmap,str):
        raise ValueError("cmap must be a string of one of the matplotlib colormaps")
    
    discretizedCmap = discretizeCmap(numberUniqueValues, cmap)

    simpleMap(
        shapefileFn, shapefileKey,
        data,
        cmap=discretizedCmap,
        colorbarType=1,
        colorbarLabels=labels,
        size=size, 
        bounds=bounds,
        title=title,
        outputFn=outputFn,
        cacheDir=cacheDir
    )

def simpleMap(shapefileFn, shapefileKey, data, cmap="Blues", colorbarRange=(None,None), colorbarType=0, colorbarLabels=None, size=(20,10), logScale=False, bounds=None, title=None, outputFn=None, cacheDir=None):
    '''

    Inputs:
    - shapefileFn: 
    - shapefileKey: 
    - data: 
    - bounds: Bounding box for the map, takes the form (south, north, west, east), i.e. (minLat, maxLat, minLon, maxLon). Defaults to the bounds from the shapefile.
    - title: Title of the map. Defaults to no title.
    - outputFn: If `None` then the figure will be displayed with plt.show(), else the figure will be saved to this filename.
    '''

    if cacheDir is None:
        cacheDir = DEFAULT_CACHE_LOCATION

    #--------------------------------------------------------------------------------------------------
    # Setup Figure
    #--------------------------------------------------------------------------------------------------
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg='#ffffff', frame_on=False)

    lats, lons = None, None
    if bounds is None:
        lats, lons = getBounds(shapefileFn)
    else:
        lats = (bounds[0],bounds[1])
        lons = (bounds[2],bounds[3])

    basemapArgs = {
        "projection":"merc",
        "llcrnrlat":lats[0],
        "urcrnrlat":lats[1],
        "llcrnrlon":lons[0],
        "urcrnrlon":lons[1],
        "resolution":"i",
        "fix_aspect":True,
        "suppress_ticks":True,
        #-------------------------------
        "cacheDir":cacheDir,
        "verbose":True
    }

    m = BasemapWrapper(**basemapArgs)

    #--------------------------------------------------------------------------------------------------
    # Load polygons with cache aware technique
    #--------------------------------------------------------------------------------------------------
    patches, keys, bounds = PolygonPatchesWrapper(
        m,
        shapefileFn, shapefileKey,
        filterList=None,
        basemapArgs=basemapArgs,
        cacheDir=cacheDir, 
        verbose=True
    )

    for patch in patches:
        patch.set_linewidth(0.5)

    p = matplotlib.collections.PatchCollection(patches, match_original=True)

    #--------------------------------------------------------------------------------------------------
    # Deal with the colorbar
    #--------------------------------------------------------------------------------------------------
    if colorbarType==0:
        #----------------------------------------------------------------
        # Single colorbar
        #----------------------------------------------------------------

        dataMin = min(data.values())
        dataMax = max(data.values())
        if colorbarRange is not None:
            if colorbarRange[0] is not None:
                dataMin = colorbarRange[0]

            if colorbarRange[1] is not None:
                dataMax = colorbarRange[1]
        
        # Add an axes at position rect [left, bottom, width, height] where all quantities are in fractions of figure width and height. 
        cbaxes = fig.add_axes([0.2, 0.03, 0.6, 0.05])

        if isinstance(cmap, str):
            cmap = matplotlib.cm.get_cmap(cmap)

        mappable = singleColorbar(cbaxes, dataMin, dataMax, cmap=cmap, logScale=logScale)

    elif colorbarType==1: #Discrete colorbar
        #----------------------------------------------------------------
        # Discrete colorbar
        #----------------------------------------------------------------

        # Add an axes at position rect [left, bottom, width, height] where all quantities are in fractions of figure width and height. 
        cbaxes = fig.add_axes([0.2, 0.03, 0.6, 0.05])

        #transform data into category format
        uniqueDataValues = sorted(list(set(data.values())))
        uniqueDataValuesMap = {val:i for i,val in enumerate(uniqueDataValues)}
        numCategories = len(uniqueDataValues)
        data = {k: uniqueDataValuesMap[v] for k,v in data.items()}

        if isinstance(cmap, str):
            raise ValueError("Must pass in an actual cmap object when using a discrete colormap (colorbarType==1)")

        mappable = discreteColorbar(cbaxes,numCategories,cmap,labels=colorbarLabels)
    else:
        raise ValueError("colorbarType has to be either 1 or 2")
    #--------------------------------------------------------------------------------------------------
    # Apply the colors
    #--------------------------------------------------------------------------------------------------   
    faceColorValues = []
    for key in keys:
        color = mappable.to_rgba(data[key])
        faceColorValues.append(color)
    
    p.set_facecolor(faceColorValues)
    ax.add_collection(p)

    #--------------------------------------------------------------------------------------------------
    # Misc Options
    #--------------------------------------------------------------------------------------------------
    padding = 2
    (xMin,xMax), (yMin, yMax) = bounds
    ax.set_xlim([xMin-padding,xMax+padding])
    ax.set_ylim([yMin-padding,yMax+padding])

    ax.tick_params(axis='both', which='both', labelsize=20)
    ax.tick_params(
        bottom=False, top=False, left=False, right=False, 
        labelbottom=False, labeltop=False, labelleft=False, labelright=False
    )
    ax.grid(b=False)

    m.drawmapboundary(
        color='k',
        linewidth=0.0,
        fill_color='#ffffff',
        zorder=None,
        ax=ax
    )

    if title is not None:
        ax.set_title(title,fontsize=26,color='k')
    
    fig.set_size_inches(size[0], size[1])
    
    if outputFn is not None:
        plt.savefig(outputFn, dpi=150, alpha=True, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


if __name__ == "__main__":
    shapefileFn = "examples/cb_2015_us_county_500k_clipped/cb_2015_us_county_500k_clipped.shp"
    shapefileKey = "GEOID"

    startTime = float(time.time())
    data = getShapefileColumn(shapefileFn, dataHeader="ALAND", primaryKeyHeader=shapefileKey)
    print "Finished loading data in %0.4f seconds" % (time.time()-startTime)

    startTime = float(time.time())
    simpleMap(shapefileFn, shapefileKey, data, outputFn="test.png", title="Land Area of Counties in the US", logScale=False)
    print "Finished drawing map in %0.4f seconds" % (time.time()-startTime)

    startTime = float(time.time())
    categoryData = {k: np.random.randint(0,5) for k,v in data.items()}
    simpleBinnedMap(shapefileFn, shapefileKey, categoryData, labels=["1","2","3","4","5"], outputFn="testCategories.png")
    print "Finished drawing map in %0.4f seconds" % (time.time()-startTime)
    
