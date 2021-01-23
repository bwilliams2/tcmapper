import os
import pandas as pd

def polygon_search(polygon_wkt: str):
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
        polygon = f"'SRID=4326;{polygon_wkt}'::geography"
        cursor.execute(f"SELECT * FROM parcels p WHERE ST_Within(p.geom_c, {polygon})")
        d = cursor.fetchall()
        data = pd.DataFrame(d).drop(columns=["geom", "geom_c"])
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return data