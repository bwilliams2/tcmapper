from pathlib import Path
import glob
from importlib.resources import path, contents

import fiona
import numpy as np
import pandas as pd

from .distance_calc import get_distances, get_bounding_box

def address_search(longitude: float, latitude: float, distance: float):
    with path("geotools", "data") as data_dir:
        files = [bytes(Path(file).absolute()) for file in glob.glob(str(data_dir.joinpath("new_parcels/*.shp").absolute()))]
    all_distances = np.array([]) 
    county_addresses = []
    for file in files:
        with fiona.open(file.decode()) as data:
            record_length = len(data)
        distances = get_distances(file, latitude, longitude, distance, record_length)
        record_positions = np.where(distances <= distance)
        with fiona.open(file.decode()) as data:
            file_records = []
            for location in record_positions[0].tolist():
                try:
                    file_records.append(data[location]["properties"])
                except:
                    print(type(location))
                    print(location)
                    print(file)
        county_addresses += file_records
        all_distances = np.concatenate([all_distances, distances[record_positions[0]]])
    data = pd.DataFrame(county_addresses)
    data["DISTANCE"] = all_distances
    return data

def get_metro_bounds():
    with path("geotools", "data") as data_dir:
        files = [bytes(Path(file).absolute()) for file in glob.glob(str(data_dir.joinpath("new_parcels/*.shp").absolute()))]
    all_coords = []
    for file in files:
        coordinates = get_bounding_box(file)
        all_coords.append(coordinates)
    all_coords = np.vstack(all_coords)
    westBoundLong = np.min(all_coords[:,0])
    eastBoundLong = np.max(all_coords[:,2])
    northBoundLat = np.max(all_coords[:,1])
    southBoundLat = np.min(all_coords[:,3])
    bounds = np.array([
        [westBoundLong, southBoundLat],
        [eastBoundLong, northBoundLat]
    ])
    return bounds
