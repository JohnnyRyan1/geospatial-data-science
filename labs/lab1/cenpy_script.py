#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Example script for Lab #1 (GEOG5/590) Geospatial Data Science Applications

"""

# Import modules
from cenpy import products
import matplotlib.pyplot as plt

###############################################################################
# Unemployment in Lane County, Oregon
###############################################################################

# Define product
acs = products.ACS()

# Print list of tables
acs.filter_tables('EMPLOYMENT', by='description')

# Print list of variables
acs.filter_variables('B23025')

# Download data
lane = products.ACS(2019).from_county('Lane County, OR', level='tract',
                                        variables=['B23025_003E', 'B23025_005E'])

# Compute unemployment percentage
lane['percent_unemployed'] = lane['B23025_005E'] / lane['B23025_003E'] * 100

# Caluclate some stats
lane['percent_unemployed'].describe()

# Plot map
f, ax = plt.subplots(1, 1, figsize=(10,10))
lane.plot('percent_unemployed', ax=ax, cmap='plasma')

# Save to file
lane.to_file('/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/labs/lab1/lane_unemployment.shp')












