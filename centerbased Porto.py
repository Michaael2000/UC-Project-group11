import geopandas as gpd
import pandas as pd
import ast
import math
import numpy as np

# print(type(start_coords[0]))

shapefile_df = gpd.read_file("Shapefile/places.shp")
loc_coord = shapefile_df["geometry"]
# print(type(loc_coord))
# print(loc_coord[0])
df_july_firstweek = pd.read_csv('df_july_firstweek.csv')
polyline_july = df_july_firstweek['POLYLINE'].apply(ast.literal_eval)


def three_closest_points(loc_coord, polylines, origin_or_destination):
    coord_list = [(x, y) for x, y in zip(loc_coord.x, loc_coord.y)]
    demand = [0] * len(coord_list)
    # print(coord_list)
    for i in range(20000):
        distances = [0] * len(coord_list)
        if origin_or_destination is True:
            coords = (polylines[i][0][0], polylines[i][0][1])
        else:
            coords = (polylines[i][-1][0], polylines[i][-1][1])

        for j in range(len(coord_list)):
            distances[j] = math.dist(coords, coord_list[j])

        top_three = np.argsort(distances)[:3]
        demand[top_three[0]] += 1
        demand[top_three[1]] += 1
        demand[top_three[2]] += 1

    return demand


origin_or_destination = True
demand = three_closest_points(loc_coord, polyline_july, origin_or_destination)
print(demand)
