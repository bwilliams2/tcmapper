from pathlib import Path
import glob

import fiona

from .distance_calc import get_distances

def address_search(longitude: float, latitude: float, distance: float):
    files = [bytes(Path(file).absolute()) for file in glob.glob("../../../data/*.shp")]
    county_addresses = []
    for file in files:
        data = fiona.open(str(file))
        record_length = len(data)
        distances = get_distances(file, longitude, latitude, distance, record_length)
        record_positions = distances[:, 0]
        file_records = [data[i]["properties"] for i in record_positions]
        county_addresses += file_records
    return county_addresses

