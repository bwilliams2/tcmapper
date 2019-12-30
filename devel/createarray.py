import fiona
from geopy.distance import geodesic
from pyproj import Proj, transform
import numpy as np
import multiprocessing as mp
import logging
import sys
from tqdm import tqdm
from pathlib import Path

original = Proj("epsg:26915")
destination = Proj("epsg:4326")


def get_long_lat(coors):
    return transform(original, destination, coors[0], coors[1])[::-1]


def main():

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    manager = mp.Manager()
    q = manager.Queue()
    with fiona.open("../data/shp_loc_address_points/AddressPoints.shp") as source:

        # Copy the source schema and add two new properties.
        sink_schema = source.schema

        # Create a sink for processed features with the same format and
        # coordinate reference system as the source.
        with tqdm(total=len(source)) as pbar:
            with open("../data/longlat.txt", "w") as f:
                for (n, loc) in enumerate(source):
                    long, lat = loc["geometry"]["coordinates"]
                    f.write(f"{long} {lat}\n")

                    if n != 0 and n % 100 == 0:
                        pbar.update(100)


if __name__ == "__main__":
    main()
