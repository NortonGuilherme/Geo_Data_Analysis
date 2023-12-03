import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from pyproj import Proj, transform
import numpy as np

def calculate_altitude_difference(df, src, origin_point, destinations, num_steps=40, threshold=3.0):
    in_proj = Proj(init='epsg:4326')  # CRS for latitude and longitude
    out_proj = Proj(src.crs)

    # Transformed coordinates for the origin point
    x_origin, y_origin = transform(in_proj, out_proj, origin_point['longitude'], origin_point['latitude'])

    # Iterate over destination points
    for i, destination in enumerate(destinations):
        # Transformed coordinates for the destination point
        x_dest, y_dest = transform(in_proj, out_proj, destination['longitude'], destination['latitude'])

        # Read raster data
        raster_data = src.read(1)

        # Initialize a list to store altitudes at each step
        altitudes_destination = []

        # Iterate over steps
        for j in range(num_steps + 1):
            # Calculate coordinates for the current point
            x_current = x_origin + (j / num_steps) * (x_dest - x_origin)
            y_current = y_origin + (j / num_steps) * (y_dest - y_origin)

            # Get altitude at the current point
            altitude_current = list(src.sample([(x_current, y_current)]))[0][0]

            # Add altitude to the list
            altitudes_destination.append(altitude_current)

        # Display altitudes at each step for the destination point
        plt.figure()
        plt.plot(np.arange(len(altitudes_destination)), altitudes_destination, 'o-', label=f'Altitudes Destination Point {i+1}')
        plt.xlabel('Steps')
        plt.ylabel('Altitude')
        plt.legend()
        plt.show()

        # Check for a hill
        max_difference = max(altitudes_destination) - min(altitudes_destination)
        if max_difference > threshold:
            print(f"There is a hill between the origin point and Destination Point {i+1}. Maximum variation: {max_difference:.2f} meters.")
        else:
            print(f"There is no hill between the origin point and Destination Point {i+1}.")

# Path to the TIFF file
tif_path = "Path/To/File.tif"

# Origin point
origin_point = {'latitude': Value, 'longitude': Value}

# List of destinations (can be a Pandas or Polars DataFrame)
destinations = [
    {'deviceID': Value, 'latitude': Value, 'longitude': Value},
    # Add more destinations as needed
]

# Open the TIFF file
with rasterio.open(tif_path) as src:
    # Calculate the altitude difference between the origin point and destinations in 40 steps
    calculate_altitude_difference(df, src, origin_point, destinations)
