import json


def read_geojson(file_path):
    """Reads a GeoJSON file and returns its content as a dictionary."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def reverse_polygon_coords(polygon):
    return [[lat, lon] for lon, lat in polygon]


def compute_centroid(polygon):
    lat_sum = sum(point[1] for point in polygon)
    lon_sum = sum(point[0] for point in polygon)
    n = len(polygon)

    return [lat_sum / n, lon_sum / n]  # [latitude, longitude]


def modify_geojson(file_path, output_path):
    """Reads a GeoJSON file, modifies coordinates, computes centroid, and saves a new file."""
    # Load GeoJSON
    geojson_data = read_geojson(file_path)

    for feature in geojson_data["features"]:
        # Extract and modify polygon coordinates
        if feature["geometry"]["type"] == "Polygon":
            original_coords = feature["geometry"]["coordinates"][
                0
            ]  # First ring (outer boundary)
            reversed_coords = reverse_polygon_coords(original_coords)
            centroid = compute_centroid(original_coords)

            # Update the feature
            feature["geometry"]["coordinates"][0] = reversed_coords
            feature["properties"]["centroid"] = centroid  # Add centroid to properties

    # Save the modified GeoJSON
    with open(output_path, "w") as f:
        json.dump(geojson_data, f, indent=4)

    print(f"Modified GeoJSON saved to: {output_path}")


modify_geojson("/tmp/pid-6494/state.geojson", "../polygons/polygon_id_5.geojson")
