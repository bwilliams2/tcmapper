from pathlib import Path
import glob
from importlib.resources import path, contents
from typing import Iterable

import fiona
from geotools.weighting import weighting_function
import numpy as np
import os
import pandas as pd
import json


# from .distance_calc import get_distances, get_bounding_box

def create_geojson(row):
    # Only keep columns used in fronted. Will need to update if more are needed
    keep_cols = ["year_built", "useclass1"]
    geojson = {
        "type": "Feature",
        "id": row["id"],
        "properties": {col.upper(): row[col] for col in keep_cols},
        "geometry": json.loads(row["parcel"])
    }
    return geojson

def _postgis_address_search(longitude: float, latitude:float, distance:float):
    import psycopg2
    import psycopg2.extras

    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    try:
        connection = psycopg2.connect(f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        gg1 = f"'SRID=4326;POINT({longitude} {latitude})'::geography"
        cursor.execute(f"SELECT *, ST_Distance({gg1}, p.geom_c) as distance, ST_AsGeoJSON(p.geom) as parcel, ST_AsText(p.geom_c) as center FROM parcels p WHERE ST_DWithin(p.geom_c, {gg1}, {distance})")
        d = cursor.fetchall()
        data = pd.DataFrame(d).drop(columns=["geom", "geom_c", "parcel"])
        lon_lat = data["center"].str.replace("POINT\(", "").str.replace(")", "").str.split(" ", expand=True)
        data["LONGITUDE"] = lon_lat.iloc[:, 0].astype(float)
        data["LATITUDE"] = lon_lat.iloc[:, 1].astype(float)
        data.columns = [col.upper() for col in data.columns]
        county_addresses = [create_geojson(row) for row in d]
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return data, county_addresses
    

def _address_search(files: Iterable[Path], longitude: float, latitude: float, distance: float):
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
                    file_records.append(data[location])
                except:
                    print(type(location))
                    print(location)
                    print(file)
        county_addresses += file_records
        all_distances = np.concatenate([all_distances, distances[record_positions[0]]])
    data_dicts = [data["properties"] for data in county_addresses]
    data = pd.DataFrame(data_dicts)
    data["DISTANCE"] = all_distances
    return data, county_addresses

def shp_address_search(longitude: float, latitude: float, distance: float):
    with path("geotools", "data") as data_dir:
        files = [bytes(file.absolute()) for file in data_dir.joinpath("shp_plan_regional_parcels").glob("*Points.shp")]
    print(files)
    return _address_search(files, longitude, latitude, distance)

def shp_parcel_address_search(longitude: float, latitude: float, distance: float):
    with path("geotools", "data") as data_dir:
        files = [bytes(file.absolute()) for file in data_dir.joinpath("shp_plan_regional_parcels").glob("*4326.shp") if "Points" not in file.name]
    return _address_search(files, longitude, latitude, distance)

def parcel_address_search(longitude: float, latitude: float, distance: float):
    return _postgis_address_search(longitude, latitude, distance)

def weighted_address_search(longitude: float, latitude: float, distance: float):
    from geotools.weighting import weighting_function
    data, features = address_search(longitude, latitude, distance)
    d = weighting_function(data)
    data["WEIGHT"] = d
    return data, features

def weighted_parcel_address_search(longitude: float, latitude: float, distance: float):
    from geotools.weighting import weighting_function
    data, features = parcel_address_search(longitude, latitude, distance)
    d = weighting_function(data)
    data["WEIGHT"] = d
    return data, features




def get_metro_bounds():
    with path("geotools", "data") as data_dir:
        files = [bytes(Path(file).absolute()) for file in glob.glob(str(data_dir.joinpath("shp_plan_regional_parcels/*.shp").absolute()))]
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
