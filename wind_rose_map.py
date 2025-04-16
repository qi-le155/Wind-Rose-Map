#!/usr/bin/env python
# coding: utf-8

from meteostat import Stations, Daily
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.patches as mpatches
from matplotlib import rcParams
import math

# The project location
latitude = 34.5026922
longitude = 109.0175252

# Set up the time scale
start = datetime(2021, 1, 1)
end = datetime(2024, 12, 31)

# Searching for the climate station near the project location
stations = Stations()
stations = stations.nearby(latitude, longitude)
station_list = stations.fetch(10)
station_info = station_list[['name', 'latitude', 'longitude', 'elevation', 'distance']]

# Get the data from the most nearly station
station = stations.fetch(1)  
station_id = station.index[0]  

# Calculate the distance between the project site with the station, make a dicision if the data is reliable

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    return distance

for index, row in station.iterrows():
    station_lat = row['latitude']
    station_lon = row['longitude']
    
    # Calculate the distance
    distance = haversine(latitude, longitude, station_lat, station_lon)
    
    # Set threshold distance (in km), for example 10 km
    threshold_distance = 10.0 # to adjust the reliable distance for the climate data
    
    if distance > threshold_distance:
        print(f"Warning: The distance between the project site and {row['name']} is {distance:.2f} km. "
              "This might result in inaccurate data.")
    else:
        print(f"The distance between the project site and {row['name']} is {distance:.2f} km. Data is reliable.")

# Get the daily data from the nearest station
data = Daily(station_id, start, end)
df = data.fetch()

# Wash the data into summer data and winter data
df['month'] = df.index.month
# Adjustable for the summer/winter time scale
summer_months = [6, 7, 8]  # June, July, August
winter_months = [12, 1, 2]  # December, January, February
summer_data = df[df['month'].isin(summer_months)]
winter_data = df[df['month'].isin(winter_months)]

# Drop the N/A data
wind_data = df[['wdir', 'wspd']].dropna()
wind_data_su = summer_data[['wdir', 'wspd']].dropna()
wind_data_win = winter_data[['wdir', 'wspd']].dropna()

# Make sure the right time scale
start_year = wind_data.index.min().year
end_year = wind_data.index.max().year


# display the figure

# Set the font to a Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei is commonly used for Chinese
plt.rcParams['axes.unicode_minus'] = False  # This ensures minus signs are displayed correctly

ax = WindroseAxes.from_ax()
ax.bar(
    wind_data['wdir'], wind_data['wspd'],
    bins=np.arange(0, 11, 2),  # Sperate the wind speed for two levels per scale
    opening=0.8,
    edgecolor='white',
    normed=True
)
ax.set_legend()
plt.title(f"{start_year} ~ {end_year} Yearly_Wind_Rose_Map")
plt.show()

ax_su = WindroseAxes.from_ax()
ax_su.bar(
    wind_data_su['wdir'], wind_data_su['wspd'],
    bins=np.arange(0, 11, 2),  # Sperate the wind speed for two levels per scale
    opening=0.8,
    edgecolor='white',
    normed=True
)
ax_su.set_legend()
plt.title(f"{start_year} ~ {end_year} Summer_Wind_Rose_Map")
plt.show()

ax_win = WindroseAxes.from_ax()
ax_win.bar(
    wind_data_win['wdir'], wind_data_win['wspd'],
    bins=np.arange(0, 11, 2),  # Sperate the wind speed for two levels per scale
    opening=0.8,
    edgecolor='white',
    normed=True
)
ax_win.set_legend()
plt.title(f"{start_year} ~ {end_year} Winter_Wind_Rose_Map")
plt.show()







