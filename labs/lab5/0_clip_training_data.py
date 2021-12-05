#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
DESCRIPTION

Clip the Landsat imagery with training data. 

"""

# Import modules
import glob
import subprocess
import os

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/'

# Define directory with images ([:-1] because we don't need BQA band)
rasters = sorted(glob.glob(filepath + 'landsat/LC08_L1TP_045031_20200222_20200225_01_T1_B*.tif'))[:-1]

# Define destination
dest = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/training_rasters/'

# Shapefiles
water = filepath + 'training_polygons/water.shp'
snow = filepath + 'training_polygons/snow.shp'
forest = filepath + 'training_polygons/forest.shp'
grassland = filepath + 'training_polygons/grassland.shp'

def raster_clip(raster, shapefile):
    """
    Function to clip raster(s) using a shapefile. 
    
    """
    # Get path and filename seperately 
    rasterfilepath, rasterfilename = os.path.split(raster)
    # Get file name without extension            
    rasterfileshortname, rasterextension = os.path.splitext(rasterfilename)
    
    # Get path and filename seperately 
    shapefilepath, shapefilename = os.path.split(shapefile)
    # Get file name without extension            
    shapefileshortname, shapefileextension = os.path.splitext(shapefilename)
     
    print ('Clipping %s.tif with %s.shp' % (rasterfileshortname, shapefileshortname))
    
    subprocess.call(['gdalwarp', '-cutline', shapefile, '-crop_to_cutline', 
                     raster, dest + rasterfileshortname + '_' + shapefileshortname + '.tif'])
      
    return 1

for i in range(len(rasters)):
    raster_clip(rasters[i], water)
    raster_clip(rasters[i], snow)
    raster_clip(rasters[i], forest)
    raster_clip(rasters[i], grassland)





