#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Access street network data from OSM and find walking distance from Condon Hall to Autzen Stadium.

"""

# Import modules
import osmnx as ox 
import networkx as nx
import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry import LineString, MultiLineString

# Define coordinates of Condon Hall
lat_lon = (44.0451, -123.0781)

# Import walkable street network data for Eugene
g = ox.graph_from_point(lat_lon, dist=2000, network_type='walk')
fig, ax = ox.plot_graph(g, node_size=10)

# As we can see, the Fronmayer Bridge doesn't come up, let's try a custom filter
cf = """
     ["area"!~"yes"]
     ["highway"!~"motor|proposed|construction|abandoned|platform|raceway"]
     ["foot"!~"no"]
     ["service"!~"private"]
     ["access"!~"private"]
     """
g = ox.graph_from_point(lat_lon, dist=2000, custom_filter=cf)
fig, ax = ox.plot_graph(g, node_size=10)

# Convert to 
graph_proj = ox.project_graph(g)

# Get Edges and Nodes
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)

# Check projection
print("Coordinate system:", edges_proj.crs)

# Import building data for Eugene
tags = {'building': True}
buildings = ox.geometries_from_point(lat_lon, tags, dist=2000)

###############################################################################
# Reproject buildings from WGS84 to UTM zone 10
###############################################################################
buildings = buildings.to_crs(edges_proj.crs)

###############################################################################
# Get centroid of Condon Hall and Autzen Stadium
###############################################################################

condon_hall = buildings[buildings['name'] == 'Condon Hall'].reset_index()
autzen = buildings[buildings['name'] == 'Autzen Stadium'].reset_index()

condon_hall['centroid'] = condon_hall['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x))

autzen['centroid'] = autzen['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x))

# Get x and y coordinates of Condon Hall
orig_xy = (condon_hall['centroid'].y.values[0], condon_hall['centroid'].x.values[0])

# Get x and y coordinates of Autzen Stadium
target_xy = (autzen['centroid'].y.values[0], autzen['centroid'].x.values[0])

###############################################################################
# Find nearest node
###############################################################################

# Find the node in the graph that is closest to the origin point (here, we want to get the node id)
orig_node = ox.get_nearest_node(graph_proj, orig_xy, method='euclidean')

# Find the node in the graph that is closest to the target point (here, we want to get the node id)
target_node = ox.get_nearest_node(graph_proj, target_xy, method='euclidean')

###############################################################################
# Calculate the shortest path
###############################################################################
route = nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight='length')

# Plot the shortest path
fig, ax = ox.plot_graph_route(graph_proj, route, route_color='blue', 
                              route_linewidth=1)

###############################################################################
# Compute walking distance
###############################################################################
# Get the nodes along the shortest path
route_nodes = nodes_proj.loc[route]

# Create a geometry for the shortest path
route_line = LineString(list(route_nodes['geometry'].values))

# Create a GeoDataFrame
route_geom = gpd.GeoDataFrame([[route_line]], geometry='geometry', crs=edges_proj.crs, columns=['geometry'])

# Print length of route
print('Walking distance to Autzen Stadium = %.1f km' % (route_geom['geometry'].length / 1000))

###############################################################################
# Export MultiString to shapefile
###############################################################################
geoms = [edges_proj.loc[(u, v, 0), 'geometry'] for u, v in zip(route[:-1], route[1:])]
gdf = gpd.GeoDataFrame(geometry=[MultiLineString(geoms)], crs=edges_proj.crs)
gdf.to_file('/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Course/5_Exploring_Spatial_Data_II/data/route.shp')




