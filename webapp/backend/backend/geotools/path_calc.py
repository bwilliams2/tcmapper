from pathlib import Path
import glob

import fiona

from .distance_calc

def address_search(longitude: float, latitude: float, distance: float):
    files = [bytes(Path(file).absolute()) for file in glob.glob("../../../data/*.shp")]
    county_addresses = []
    for file in files:

