# -*- coding: utf-8 -*-
"""

Example of accessing Landsat Level-1 data directly from Google Cloud Storage. 

"""

# Import modules
import rasterio

# Define Google Cloud storage
base_url = 'https://storage.googleapis.com/gcp-public-data-landsat/LC08/01'

# Define Landsat path/row for Western Oregon
path = 47
row = 29

#Pre-identified cloud-free Image IDs for this path/rowin summer of 2020
img = 'LC08_L1TP_047029_20200814_20200822_01_T1'

#Loop through all bands
bands = []
for b in range(1,12):
    #Generate the appropriate URL for the images we identified
    image_url =  '{0}/{1:03d}/{2:03d}/{3}/{3}_B{4}.TIF'.format(base_url, path, row, img, b)
    bands.append(image_url)

# Read the data
with rasterio.open(bands[0]) as src:
    band_1 = src.read(1)