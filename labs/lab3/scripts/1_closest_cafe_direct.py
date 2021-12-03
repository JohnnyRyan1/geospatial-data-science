#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Access building data from OSM and find distance to nearest cafes.

"""

# Import modules
import osmnx as ox 
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import numpy as np
import pandas as pd

# Specify type of data
tags = {'building': True}
gdf = ox.geometries_from_place('Eugene, Oregon, USA', tags)

# Get a specific amenity
cafes = gdf[gdf['amenity'] == 'cafe'].reset_index()

# =============================================================================
# # Reproject WGS84 to UTM zone
# lon = gdf['geometry'].centroid[0].x
# lat = gdf['geometry'].centroid[0].y
# proj = ox.utils_geo.bbox_from_point((lat, lon), dist=500, project_utm=True, return_crs=True)
# local_utm_crs = proj[-1]
# =============================================================================
gdf = gdf.to_crs('EPSG:32610')
cafes = cafes.to_crs('EPSG:32610')

# Get coordinates of Condon Hall
condon_hall = gdf[gdf['name'] == 'Condon Hall'].reset_index()

# Get cafe centroids
cafes['centroid'] = cafes['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x))

condon_hall['centroid'] = condon_hall['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x))

# Compute distances
condon_hall_x = condon_hall['centroid'].x.values[0]
condon_hall_y = condon_hall['centroid'].y.values[0]
distances = np.sqrt(((condon_hall_x - cafes['centroid'].x.values)**2)
                     + ((condon_hall_y - cafes['centroid'].y.values)**2))

# Add to GeoDataFrame
cafes['dist'] = distances

# Find the ten closest cafes
print(cafes.nsmallest(10, ['dist'])[['name', 'dist']])

# Only keep certain columns
nearest_cafes = cafes.nsmallest(10, ['dist'])[['name', 'dist', 'centroid']]

# Relabel
nearest_cafes.rename(columns={'centroid':'geometry'}, inplace=True)

# Save to file
nearest_cafes.to_file('/Users/jryan4/Dropbox (University of Oregon)/Teaching/geospatial-data-science/labs/lab3/data/cafes.shp')





