import os
import json


def convert_json_to_geojson(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        locations = data.get("locations")
        if locations:
            features = []
            for location in locations:
                latitudeE7 = location.get("latitudeE7")
                longitudeE7 = location.get("longitudeE7")
                if latitudeE7 is not None and longitudeE7 is not None:
                    latitude = latitudeE7 / 1e7
                    longitude = longitudeE7 / 1e7
                    point = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [longitude, latitude]
                        },
                        "properties": location
                    }
                    features.append(point)
            feature_collection = {
                "type": "FeatureCollection",
                "features": features
            }
            return feature_collection
        else:
            return None


def convert_folder_json_to_geojson(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(folder_path, file_name)
            print(f"Converting {file_name} to GeoJSON...")
            geojson_data = convert_json_to_geojson(json_file_path)
            if geojson_data:
                geojson_file_name = file_name.replace('.json', '.geojson')
                geojson_file_path = os.path.join(folder_path, geojson_file_name)
                if os.path.exists(geojson_file_path):
                    os.remove(geojson_file_path)  # Remove existing GeoJSON file
                with open(geojson_file_path, 'w') as geojson_file:
                    json.dump(geojson_data, geojson_file)
                print(f"Converted {file_name} to {geojson_file_name}")
            else:
                print(f"Skipping {file_name} as it does not contain valid JSON data")


# Specify the folder path containing the JSON files
folder_path = '/Users/efigueira/Library/CloudStorage/GoogleDrive-edgarjunceiro@gmail.com/O meu disco/30daysMapChallenge/02/data/Takeout/Histórico de localizações'

# Convert JSON files to GeoJSON
convert_folder_json_to_geojson(folder_path)
