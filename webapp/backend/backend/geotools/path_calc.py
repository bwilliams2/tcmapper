from pathlib import Path
import glob
from importlib.resources import path, contents

import fiona
import numpy as np
import pandas as pd

from .distance_calc import get_distances

def address_search(longitude: float, latitude: float, distance: float):
    with path("backend", "data") as data_dir:
        files = [bytes(Path(file).absolute()) for file in glob.glob(str(data_dir.joinpath("*.shp").absolute()))]
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

