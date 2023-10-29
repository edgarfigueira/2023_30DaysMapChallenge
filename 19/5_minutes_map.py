import shapely.geometry as sg
import fiona
import matplotlib.pyplot as plt
from shapely.ops import transform
from functools import partial
import pyproj

def reproject_geometry(geometry, from_proj, to_proj):
    project = partial(
        pyproj.transform,
        pyproj.Proj(from_proj),  # source coordinate system
        pyproj.Proj(to_proj))  # destination coordinate system
    return transform(project, geometry)

def clip_by_radius(point, radius, geometry):
    buffer = point.buffer(radius)
    return geometry.intersection(buffer)

def main():
    # User inputs
    latitude = float(input("Enter latitude (decimal degrees): "))
    longitude = float(input("Enter longitude (decimal degrees): "))

    # Define the reference point and radius
    reference_point = sg.Point(longitude, latitude)
    radius = 500  # meters

    # Load shapefiles
    roads = fiona.open("roads.shp")
    buildings = fiona.open("buildings.shp")

    # Filter features within the radius
    roads = [reproject_geometry(sg.shape(road['geometry']), roads.crs, '+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs') for road in roads if sg.shape(road['geometry']).intersects(reference_point.buffer(radius))]
    buildings = [reproject_geometry(sg.shape(building['geometry']), buildings.crs, '+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs') for building in buildings if sg.shape(building['geometry']).intersects(reference_point.buffer(radius))]

    # Create a new figure
    fig, ax = plt.subplots()

    # Plot roads
    for road in roads:
        x, y = road.xy
        ax.plot(x, y, color='#000000', linewidth=1)

    # Plot buildings
    for building in buildings:
        x, y = building.exterior.xy
        ax.fill(x, y, color='#000000', linewidth=0.2)

    # Set aspect of the plot to be equal
    ax.set_aspect('equal')

    # Save the figure
    plt.savefig('output_map.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    main()
