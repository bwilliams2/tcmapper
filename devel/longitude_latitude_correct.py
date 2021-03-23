import fiona
from geopy.distance import geodesic
from pyproj import Proj, transform
import multiprocessing as mp
import logging
import sys
from pathlib import Path

original = Proj("epsg:26915")
destination = Proj("epsg:4326")


def get_long_lat(coors):
    return transform(original, destination, coors[0], coors[1])[::-1]


def worker(rec, q):

    try:
        # If any feature's polygon is facing "down" (has rings
        # wound clockwise), its rings will be reordered to flip
        # it "up".
        lat, long = get_long_lat(rec["geometry"]["coordinates"])

        # Add the signed area of the polygon and a timestamp
        # to the feature properties map.
        rec["properties"].update(dict(LONGITUDE=long, LATITUDE=lat))

        q.put(rec)

    except Exception as e:
        logging.exception("Error processing feature %s:", rec["id"])


def listener(q, crs, driver, sink_schema):
    with fiona.open(
        "data/corrected/AddressPoints-Corrected.shp",
        "w",
        crs=crs,
        driver=driver,
        schema=sink_schema,
    ) as sink:
        while True:
            m = q.get()
            if m == "kill":
                break
            sink.write(m)


def main():

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    manager = mp.Manager()
    q = manager.Queue()
    with fiona.open("data/shp_loc_address_points/AddressPoints.shp") as source:

        # Copy the source schema and add two new properties.
        sink_schema = source.schema

        # Create a sink for processed features with the same format and
        # coordinate reference system as the source.

        pool = mp.Pool(mp.cpu_count() - 2)
        watcher = pool.apply_async(
            listener, (q, source.crs, source.driver, sink_schema)
        )
        jobs = []
        for loc in source:
            job = pool.apply_async(worker, (loc, q))
            jobs.append(job)

    for job in jobs:
        job.get()

    q.put("kill")
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
