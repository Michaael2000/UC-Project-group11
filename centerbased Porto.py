import geopandas as gpd

shapefile_df = gpd.read_file("Shapefile/places.shp")
loc_coord = shapefile_df["geometry"]
print(type(loc_coord))
