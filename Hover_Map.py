import pandas as pd
import folium
import osmnx as ox
import networkx as nx
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

route_df = pd.read_csv('route_data_3.csv')

print("Columns in route_df:", route_df.columns)

X = route_df[['distance']]  
y = route_df['travel_time'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
route_df['predicted_travel_time'] = rf_model.predict(X)

map_center = [16.5062, 80.6480]  
route_map = folium.Map(location=map_center, zoom_start=13)

def get_color(travel_time):
    if travel_time < 10:
        return 'green'
    elif 10 <= travel_time < 20:
        return 'orange'
    else:
        return 'red'

for index, row in route_df.iterrows():
    start_location = (row['start_lat'], row['start_lon'])
    end_location = (row['end_lat'], row['end_lon'])
    
    color = get_color(row['predicted_travel_time'])
    
    folium.PolyLine(locations=[start_location, end_location], color=color, weight=6, opacity=0.7).add_to(route_map)
    folium.Marker(
        location=end_location,
        popup=f'Predicted Travel Time: {row["predicted_travel_time"]:.2f} minutes',
        tooltip=row['end_name'], 
        icon=folium.Icon(color=color)
    ).add_to(route_map)

legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 100px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white;">
    &nbsp; <b>Travel Time Legend</b> <br>
    &nbsp; <i class="fa fa-circle" style="color:green"></i>&nbsp; < 10 mins <br>
    &nbsp; <i class="fa fa-circle" style="color:orange"></i>&nbsp; 10-20 mins <br>
    &nbsp; <i class="fa fa-circle" style="color:red"></i>&nbsp; > 20 mins <br>
    </div>'''
route_map.get_root().html.add_child(folium.Element(legend_html))

route_map.save('amaravati_routes_with_predictions01.html')
print("amaravati_routes_with_predictions.html has been generated with predicted travel times.")

G = ox.graph_from_place('Amaravati, Andhra Pradesh, India', network_type='drive')

if not route_df.empty:
    start_lat, start_lon = route_df.iloc[0]['start_lat'], route_df.iloc[0]['start_lon']
    end_lat, end_lon = route_df.iloc[0]['end_lat'], route_df.iloc[0]['end_lon']
    
    start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)
    end_node = ox.distance.nearest_nodes(G, X=end_lon, Y=end_lat)

    shortest_path = nx.shortest_path(G, start_node, end_node)
    ax = ox.plot_graph(G, node_color='red', edge_color='lightblue', show=False, close=False, edge_linewidth=0.5)  
    route_line = [(G.nodes[node]['x'], G.nodes[node]['y']) for node in shortest_path]
    plt.plot(*zip(*route_line), color='lightcoral', linewidth=10) 

    for node in shortest_path:
        x, y = G.nodes[node]['x'], G.nodes[node]['y']
        place_name = G.nodes[node].get('name', f'Node {node}')  
        plt.annotate(place_name, (x, y), textcoords="offset points", xytext=(0, 20), ha='center', fontsize=12, color='black') 

    plt.title('Optimized Route on Colorful Map', fontsize=24)  
    plt.xlabel('Longitude', fontsize=18)  
    plt.ylabel('Latitude', fontsize=18) 
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.savefig('optimized_route_color_map01.png', dpi=300)  
    plt.close() 
    print("Colorful map with optimized route saved as optimized_route_color_map01.png.")