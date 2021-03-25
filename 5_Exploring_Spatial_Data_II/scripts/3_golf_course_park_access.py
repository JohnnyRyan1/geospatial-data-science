#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""

# Import modules
import osmnx as ox
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Define EPSG code for Oregon
epsg = 'EPSG:32610'

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM/data/'

# Import city boundary data
city = gpd.read_file(filepath + 'city/city.shp')
city = city[city['SUM_TAPERS'] > 10000]
city = city.to_crs(epsg)
city['area_city'] = city['geometry'].area

# Search for areas tagged as leisure within a certain distance of point
tags = {'leisure': True}
areas = ox.geometries_from_place('Oregon, USA', tags)

# Get areas labeled as golf course
golf_courses = areas[areas['leisure'] == 'golf_course']

# Get areas labeled as parks
parks = areas[areas['leisure'] == 'park']

# Get just polygons
golf_courses = golf_courses[(golf_courses['geometry'].geom_type == 'Polygon')]
parks = parks[(parks['geometry'].geom_type == 'Polygon')]

# Export to file
golf_gdf = gpd.GeoDataFrame(geometry=list(golf_courses['geometry']), crs=4326)
golf_gdf = golf_gdf.to_crs(epsg)
golf_gdf['area_golf'] = golf_gdf['geometry'].area
golf_gdf.to_file(filepath + 'golf_courses_oregon.shp')

park_gdf = gpd.GeoDataFrame(geometry=list(parks['geometry']), crs=4326)
park_gdf = park_gdf.to_crs(epsg)
park_gdf['area_park'] = park_gdf['geometry'].area
park_gdf.to_file(filepath + 'parks_oregon.shp')

# Intersect parks with city boundaries
parks_within = gpd.sjoin(park_gdf, city, how="inner", op='intersects')

# Intersect golf courses with city boundaries
golf_within = gpd.sjoin(golf_gdf, city, how="inner", op='intersects')

city_name = []
city_area = []
city_pop = []
park_area = []
golf_area = []
park_num = []
golf_num = []

for i in parks_within['AREANAME'].unique():
    city_name.append(i)
    city_area.append(parks_within[parks_within['AREANAME'] == i]['area_city'].iloc[0] / 1000000)
    city_pop.append(parks_within[parks_within['AREANAME'] == i]['SUM_TAPERS'].iloc[0])
    park_num.append(parks_within[parks_within['AREANAME'] == i].shape[0])
    golf_num.append(golf_within[golf_within['AREANAME'] == i].shape[0])
    park_area.append(parks_within[parks_within['AREANAME'] == i]['area_park'].sum() / 1000000)
    golf_area.append(golf_within[golf_within['AREANAME'] == i]['area_golf'].sum()  / 1000000)


# Put into DataFrame
df = pd.DataFrame(list(zip(city_name, city_area, city_pop, park_area, golf_area,
                           park_num, golf_num)))
df.columns = ['city_name', 'city_area', 'city_pop', 'park_area', 'golf_area',
              'park_num', 'golf_num']


fig, ax = plt.subplots()
ax.scatter(df['park_area'], df['golf_area'])

for i, txt in enumerate(df['city_name']):
    ax.annotate(txt, (df['park_area'].iloc[i], df['golf_area'].iloc[i]))

plt.xlabel('Park area (km2)')
plt.ylabel('Golf course area (km2)')









