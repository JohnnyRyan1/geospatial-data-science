#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Explore Landsat imagery and generate training data.

"""

# Import modules
import numpy as np
import glob
import os
from osgeo import gdal

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/landsat/' 

# Define image list
images_winter = sorted(glob.glob(filepath + 'LC08_L1TP_045031_20200222_20200225_01_T1_*.tif'))

# Define some functions
def geotiff_read(infile):
    """ 
    Function to read a GeoTIFF file and convert to numpy array.
    
    """
    # Allow GDAL to throw Python exceptions
    gdal.UseExceptions()
    
    print('Reading %s' % infile)
    # Read tiff and convert to a numpy array
    tiff = gdal.Open(infile)
    
    if tiff.RasterCount == 1:
        array = tiff.ReadAsArray()
    
    if tiff.RasterCount > 1:
        array = np.zeros((tiff.RasterYSize, tiff.RasterXSize, tiff.RasterCount))
        for i in range(tiff.RasterCount):
            band = tiff.GetRasterBand(i + 1)            
            array[:, :, i] = band.ReadAsArray()
    
    # Get parameters    
    geotransform = tiff.GetGeoTransform()
    projection = tiff.GetProjection()
    band = tiff.GetRasterBand(1)
    nodata = band.GetNoDataValue()
   
    return array, geotransform, projection, nodata





















