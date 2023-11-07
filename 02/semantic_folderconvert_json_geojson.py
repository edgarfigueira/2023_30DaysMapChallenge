import os
import json

def convert_json_to_geojson(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        timeline_objects = data["timelineObjects"]
        features = []
        for timeline_obj in timeline_objects:
            place_visit = timeline_obj.get("placeVisit")
            if place_visit:
                location = place_visit.get("location")
                if location:
                    latitudeE7 = location.get("latitudeE7")
                    longitudeE7 = location.get("longitudeE7")
                    address = location.get("address")
                    if latitudeE7 is not None and longitudeE7 is not None:
                        latitude = latitudeE7 / 1e7
                        longitude = longitudeE7 / 1e7
                        point = {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [longitude, latitude]
                            },
                            "properties": {
                                "address": address
                            }
                        }
                        features.append(point)
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }
        return feature_collection


def convert_folder_json_to_geojson(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(folder_path, file_name)
            geojson_data = convert_json_to_geojson(json_file_path)
            geojson_file_name = file_name.replace('.json', '.geojson')
            geojson_file_path = os.path.join(folder_path, geojson_file_name)
            with open(geojson_file_path, 'w') as geojson_file:
                json.dump(geojson_data, geojson_file)
            print(f"Converted {file_name} to {geojson_file_name}")


# Specify the folder path containing the JSON files
folder_path = '/Users/efigueira/4_brincadeiras/Takeout/Location History/Semantic Location History/2013'


# Convert JSON files to GeoJSON
convert_folder_json_to_geojson(folder_path)
