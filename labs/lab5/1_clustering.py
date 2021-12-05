#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Perform KMeans clustering to predict land cover classes.

"""

# Import modules
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import glob
import gdal

# Define some functions
def geotiff_read(infile):
    """ 
    Function to read a Geotiff file and convert to numpy array.
    
    """
    # Allow GDAL to throw Python exceptions
    gdal.UseExceptions()
    
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

def geotiff_write(outfile, geotransform, projection, data, nodata=None):
    """
    Function to write a numpy array as a GeoTIFF file.
    
    IMPORTANT: I've edited this function so it writes the data as byte format.
    
    """
    # Produce numpy to GDAL conversion dictionary    
    print('Writing %s' % outfile)
    driver = gdal.GetDriverByName('GTiff')
    
    if data.ndim == 2:
        (x,y) = data.shape
        tiff = driver.Create(outfile, y, x, 1, gdal.GDT_Byte)
        tiff.GetRasterBand(1).WriteArray(data)
       
    if data.ndim > 2:
        bands = data.shape[2]
        (x,y,z) = data.shape
        tiff = driver.Create(outfile, y, x, bands, gdal.GDT_Byte)
        for band in range(bands):
            array = data[:, :, band + 1]
            tiff.GetRasterBand(band).WriteArray(array)
    
    if nodata:
        tiff.GetRasterBand(1).SetNoDataValue(nodata)
    tiff.SetGeoTransform(geotransform)
    tiff.SetProjection(projection) 
    tiff = None	
    
    return 1

###############################################################################
# Import data
###############################################################################

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/'

# Define Landsat image
landsat = sorted(glob.glob(filepath + 'landsat/LC08_L1TP_045031_20200222_20200225_01_T1_B*.tif'))[:-1]

samples = []

for i in landsat:
    # Read training rasters
    array, geotransform, projection, nodata = geotiff_read(i)

    # Put data into the right shadf = shuffle(df)pe
    samples.append(list(np.ravel(array)))
    
# Put into DataFrame
df = pd.DataFrame(list(zip(samples[0], samples[1], samples[2], 
                           samples[3], samples[4], samples[5], 
                           samples[6], samples[7], samples[8], 
                           samples[9])))

df.columns = ['B1', 'B10', 'B11', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']

# Swap some columns
df = df[['B10', 'B11', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']]

# Shuffle
df_shuffled = shuffle(df)

###############################################################################
# Visualize data
###############################################################################

plt.scatter(df['B1'], df['B6'])
plt.xlabel('B1')
plt.ylabel('B6')

###############################################################################
# Perform clustering
###############################################################################

# Define number of clusters
Kmean = KMeans(n_clusters=8)

# Fit to dataset
Kmean.fit(df_shuffled[::50])

# Find centroids of clusters
Kmean.cluster_centers_

plt.scatter(df[::100]['B1'], df[::100]['B6'], s=50, color='lightblue')
plt.scatter(Kmean.cluster_centers_[0][2],Kmean.cluster_centers_[0][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[1][2],Kmean.cluster_centers_[1][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[2][2],Kmean.cluster_centers_[2][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[3][2],Kmean.cluster_centers_[3][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[4][2],Kmean.cluster_centers_[4][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[5][2],Kmean.cluster_centers_[5][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[6][2],Kmean.cluster_centers_[6][7], s=100, c='red', marker='s')
plt.scatter(Kmean.cluster_centers_[7][2],Kmean.cluster_centers_[7][7], s=100, c='red', marker='s')
plt.xlabel('B1')
plt.ylabel('B6')

###############################################################################
# Predict the rest of image using Kmeans clustering
###############################################################################

# Predict
predictions = Kmean.predict(df)

# Reshape
p = predictions.reshape(array.shape[0], array.shape[1])

# Write classified array as an GeoTIFF
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/classifications/'
geotiff_write(filepath + 'classified_kmeans.tif', 
              geotransform, projection, p)











