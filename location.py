import osmnx as ox
import pandas as pd

city_name = "Amaravati, Andhra Pradesh, India"
tags = {"amenity": True} 
locations = ox.geometries_from_place(city_name, tags)

df = locations.reset_index()[["name", "geometry"]]

df["Latitude"] = df["geometry"].apply(lambda x: x.centroid.y if x else None)
df["Longitude"] = df["geometry"].apply(lambda x: x.centroid.x if x else None)

df = df.dropna(subset=["Latitude", "Longitude", "name"])
df = df[["name", "Latitude", "Longitude"]]
df.columns = df.columns.str.lower() 

file_name = "amaravati_osm_locations01.csv"
df.to_csv(file_name, index=False)
print(f"Data saved to '{file_name}'.")