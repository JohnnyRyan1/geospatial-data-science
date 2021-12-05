#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Predict land cover classes using Random Forests algorithm.

"""

# Import modules
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import glob
import gdal

###############################################################################
# Import data
###############################################################################

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/training_data/'

# Import data
training_data = pd.read_csv(filepath + 'training_data.csv')

###############################################################################
# Prepare data
###############################################################################

# Define feeature list 
feature_list = ['B10', 'B11', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']

# Define labels and targets
y = training_data['label']
X = training_data.loc[:, training_data.columns != 'label']

###############################################################################
# Visualize data
###############################################################################

plt.scatter(X[y==1]['B1'], X[y==1]['B6'], color='blue', zorder=2)
plt.scatter(X[y==2]['B1'], X[y==2]['B6'], color='yellow', zorder=2)
plt.scatter(X[y==3]['B1'], X[y==3]['B6'], color='darkgreen', zorder=1)
plt.scatter(X[y==4]['B1'], X[y==4]['B6'], color='lightgreen', zorder=2)
plt.xlabel('B1')
plt.ylabel('B6')

###############################################################################
# Perform machine learning using Random Forests
###############################################################################

# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Define classifier
classifier = RandomForestClassifier(n_estimators=100)

# Train classifier
classifier.fit(X_train, y_train)

# Predict
predictions = classifier.predict(X_test)

###############################################################################
# Evaluate model
###############################################################################

print("Completed training and testing model...")
print("Fraction Correct")
print(np.sum(predictions == y_test) / float(len(y_test)))
   
# Classification Report
target_names = ['Null', 'Water', 'Snow', 'Forest', 'Grassland']
print(classification_report(y_test, predictions, target_names=target_names))
    
# Confusion matrix
cmat = confusion_matrix(y_test, predictions)
   
# The fraction of correctly classified labels 
fraction = cmat.diagonal() / cmat.sum(axis=1)

# Plot confusion matrix
plot_confusion_matrix(classifier, X_test, y_test)

# F1 score?

###############################################################################
# Apply model to Landsat image
###############################################################################
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

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/'

# Define Landsat image
landsat = sorted(glob.glob(filepath + 'landsat/LC08_L1TP_045031_20200222_20200225_01_T1_B*.tif'))[:-1]

samples = []

for i in landsat:
    # Read training rasters
    array, geotransform, projection, nodata = geotiff_read(i)

    # Put data into the right shape
    samples.append(list(np.ravel(array)))
    
# Put into DataFrame
df = pd.DataFrame(list(zip(samples[0], samples[1], samples[2], 
                           samples[3], samples[4], samples[5], 
                           samples[6], samples[7], samples[8], 
                           samples[9])))

df.columns = ['B1', 'B10', 'B11', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']

# Swap some columns
df = df[['B10', 'B11', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']]

# Perform classification
pred_y = classifier.predict(df.astype(float))
p = pred_y.reshape(array.shape[0], array.shape[1])

# Write classified array as an GeoTIFF
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/Land_Cover_Classification/data/classifications/'
geotiff_write(filepath + 'classified_rf.tif', 
              geotransform, projection, p)











