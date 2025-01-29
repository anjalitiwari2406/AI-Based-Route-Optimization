import pandas as pd
import numpy as np
import random

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

locations_df = pd.read_csv('amaravati_osm_locations01.csv')
locations = list(zip(locations_df['latitude'], locations_df['longitude'], locations_df['name']))
route_data = []

for i in range(len(locations)):
    for j in range(len(locations)):
        if i != j: 
            start_lat, start_lon, start_name = locations[i]
            end_lat, end_lon, end_name = locations[j]
            distance = haversine(start_lat, start_lon, end_lat, end_lon)
            travel_time = (distance / 30) * 60 + random.uniform(-2, 5) 
            travel_time = max(1, travel_time)  
            route_data.append({
                'start_lat': start_lat,
                'start_lon': start_lon,
                'start_name': start_name,
                'end_lat': end_lat,
                'end_lon': end_lon,
                'end_name': end_name,
                'distance': round(distance, 2), 
                'travel_time': round(travel_time, 2)  
            })

route_df = pd.DataFrame(route_data)
route_df.to_csv('route_data_3.csv', index=False)
print("route_data_2.csv has been generated with all locations in Amaravati, including distance, travel time, and location names.")