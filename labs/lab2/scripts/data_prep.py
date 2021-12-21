#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Prepare wildfire data

"""

# Import modules
import pandas as pd
import geopandas as gpd
from geopandas.tools import clip

# Define path to wildfire data
path = '/Users/jryan4/Dropbox (University of Oregon)/Teaching/490_Geospatial_Data_Science_Applications/data_preparation/Wildfires/us_1992-2018.shp'

# Define path to state shapefile
state = '/Users/jryan4/Dropbox (University of Oregon)/Teaching/490_Geospatial_Data_Science_Applications/data_preparation/shapfiles/cb_2018_us_state_20m.shp'

# Read data
df = gpd.read_file(path)
states = gpd.read_file(state)

# Convert to WGS84
states = states.to_crs('EPSG:4326')

# Get indivudual states
ore = states[states['STATEFP'] == '41']
cal = states[states['STATEFP'] == '06']
was = states[states['STATEFP'] == '53']

# Clip by polygon
points_ore = clip(df, ore)
points_cal = clip(df, cal)
points_was = clip(df, was)

# Save to file
points_ore.to_file('/Users/jryan4/Dropbox (University of Oregon)/Teaching/490_Geospatial_Data_Science_Applications/data_preparation/Wildfires/or_1992-2018.shp')

