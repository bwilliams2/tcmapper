from pathlib import Path
import glob
from typing import Iterable

import fiona
import numpy as np
import os
import pandas as pd
import json

def create_geojson(row):
    # Only keep columns used in fronted. Will need to update if more are needed
    parcel = row.pop("parcel")
    geojson = {
        "type": "Feature",
        "id": row["id"],
        "properties": row,
        "geometry": json.loads(parcel)
    }
    return geojson

def all_election_data(year: int):
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
        cursor.execute(f"SELECT *, ST_AsGeoJSON(p.geom) as parcel FROM processed_election p WHERE p.year = {year}")
        d = cursor.fetchall()
        data = pd.DataFrame(d).drop(columns=["geom", "geom_c", "parcel"])
        data.columns = [col for col in data.columns]
        features = [create_geojson(row) for row in d]
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return data, features
    
