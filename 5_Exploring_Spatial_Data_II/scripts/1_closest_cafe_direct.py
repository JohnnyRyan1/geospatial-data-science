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

# Specify type of data
tags = {'building': True}
gdf = ox.geometries_from_place('Eugene, Oregon, USA', tags)

###############################################################################
# Reproject WGS84 to UTM zone
###############################################################################
lon = gdf['geometry'].centroid[0].x
lat = gdf['geometry'].centroid[0].y
proj = ox.utils_geo.bbox_from_point((lat, lon), dist=500, project_utm=True, return_crs=True)
local_utm_crs = proj[-1]
gdf = gdf.to_crs(local_utm_crs)

###############################################################################
# Get a specific amenity
###############################################################################
cafe = gdf[gdf['amenity'] == 'cafe'].reset_index()

###############################################################################
# Reproject WGS84 to UTM zone
###############################################################################
# Get coordinates of Condon Hall
condon_hall = gdf[gdf['name'] == 'Condon Hall'].reset_index()

# Get cafe centroids
cafe['centroid'] = cafe['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x))

condon_hall['centroid'] = condon_hall['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x))

# Compute distances
condon_hall_x = condon_hall['centroid'].x.values[0]
condon_hall_y = condon_hall['centroid'].y.values[0]
distances = np.sqrt(((condon_hall_x - cafe['centroid'].x.values)**2)
                     + ((condon_hall_y - cafe['centroid'].y.values)**2))

# Add to GeoDataFrame
cafe['dist'] = distances

# Find the ten closest cafes
print(cafe.nsmallest(10, ['dist'])[['name', 'dist']])








