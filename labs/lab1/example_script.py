#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Download Census Bureau data.

Cloned from: 
    https://github.com/jtleider/censusdata

Variables for block groups here:
    https://api.census.gov/data/2019/acs/acs5/variables.html
    
Excellent guide can be found here:
    https://api.census.gov/data.html

"""

# Import modules
import censusdata
import geopandas as gpd
import pandas as pd


# Define path to save
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Print table showing variables for employment status
censusdata.printtable(censusdata.censustable('acs5', 2019, 'B23025'))

# Print table showing state FIPS
censusdata.geographies(censusdata.censusgeo([('state', '*')]), 'acs5', 2019)

# Print table showing County codes
censusdata.geographies(censusdata.censusgeo([('state', '41'), ('county', '*')]), 'acs5', 2019)

# Download data
lane_tract = censusdata.download('acs5', 2019,
                             censusdata.censusgeo([('state', '41'), ('county', '039'), 
                                                   ('tract', '*')]), ['B23025_003E', 'B23025_005E'])

# Compute unemployment percentage
lane_tract['percent_unemployed'] = lane_tract['B23025_005E'] / lane_tract['B23025_003E'] * 100

# Sort values
lane_tract.sort_values('percent_unemployed', ascending=False).head(30)

# Compute some statistics

###############################################################################
# Merge with shapefile to find where these are located
###############################################################################

# Read shapefile
shapefile = gpd.read_file('/home/johnny/Downloads/tl_2021_41_tract/tl_2021_41_tract.shp')

# Get tract attribute column
tract = []
for i in range(lane_tract.shape[0]):
    tract.append(lane_tract.index[i].geo[2][1])
    
# Edit some column names so they match the shapefile
lane_tract['TRACTCE'] = tract
lane_tract['COUNTYFP'] = '039'
    
# Merge DataFrames
lane_gdf = pd.merge(left=shapefile, right=lane_tract, on=(['COUNTYFP', 'TRACTCE']))

# Save as shapefile
lane_gdf.to_file('/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/labs/lab1/lane_unemployment.shp')








