# Populate docker postgis database
# pscopg2 connection, replace *** and *** with your values
from ast import parse
import psycopg2
import re
import fiona
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
import argparse
import os
import json
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
load_dotenv()

def check_db():
    try:
        connection = psycopg2.connect(f"user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'commutedb'")
        db_exists = cursor.fetchone()
        if not db_exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier("commutedb")))
            connection.commit()
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return

def parse_columns(schema):
    columns = []
    for name, value in schema["properties"].items():
        if "LONGITUDE" == name or "LATITUDE" == name:
            continue
        if  "str" in value:
            val_type = "VARCHAR"
        elif "int" in value:
            val_type = "INTEGER"
        elif "float" in value:
            val_type = "DOUBLE PRECISION"
        columns.append(f"{name} {val_type}")
    return columns

    
def convert_polygon(polygons):
    all_shapes = []
    for polygon in polygons:
        poly = [" ".join([str(item) for item in sublist]) for sublist in polygon]
        poly = f'(({", ".join(poly)}))'
        all_shapes.append(poly)
    return f"{','.join(all_shapes)}"

def values_factory(parsed_columns):
    def process_values(row):
        values = []
        for col in parsed_columns:
            value = row["properties"].get(col.split(" ")[0])
            if value is None:
                values.append("NULL")
            elif "VARCHAR" in col:
                value = value.replace("'", "")
                values.append(f"'{value}'")
            elif "INTEGER" in col:
                values.append(str(int(value)))
            elif "DOUBLE" in col:
                values.append(str(float(value)))
            else:
                values.append(str(value))
        return values
    return process_values

def populate_parcels():
    try:
        files = [file for file in Path("../../data/shp_plan_regional_parcels").glob("*4326.shp") if "Points" not in file.name]
        data = fiona.open(files[0])
        parsed_columns = parse_columns(data.schema)
        columns = ",".join(["id SERIAL"] + parsed_columns)
        connection = psycopg2.connect(f"dbname=postgres user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS parcels")
        cursor.execute(f"""
            CREATE TABLE parcels (
                {columns},
                parcel_area DOUBLE PRECISION,
                geom GEOGRAPHY(MULTIPOLYGON),
                geom_c GEOGRAPHY(Point),

                PRIMARY KEY (id))
        """)

        # cursor.execute("""
        #     SELECT AddGeometryColumn('parcels', 'geom', 4326, 'MULTIPOLYGON', 2)
        # """)

        # cursor.execute("""
        #     SELECT AddGeometryColumn('parcels', 'geom_c', 4326, 'POINT', 2)
        # """)

        def process_values(row):
            values = []
            for col in parsed_columns:
                value = row["properties"][col.split()[0]]
                if value is None:
                    values.append("NULL")
                elif "VARCHAR" in col:
                    value = value.replace("'", "")
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))
            return values


        # use arcpy to get attribute data, populate PostGIS using psycopg2
        cols = [col.split()[0] for col in parsed_columns]
        for file in files:
            data = fiona.open(file)
            print(f"\nProcessing parcels from {file.name}")
            for n, row in tqdm(enumerate(data), total=len(data)):
                if row["properties"]["VIEWID"] == 130605:
                    continue
                if row["geometry"]["type"] == "MultiPolygon":
                    parcel = ",".join([convert_polygon(shape) for shape in row["geometry"]["coordinates"]])
                else:
                    parcel = convert_polygon(row["geometry"]["coordinates"])
                if row["properties"]["LONGITUDE"] == float("inf"):
                    point_entry = "NULL"
                else:
                    point = str(row["properties"]["LONGITUDE"]) + " " + str(row["properties"]["LATITUDE"])
                    # point_entry = f"ST_GeometryFromText('POINT({point})', 4326)"
                    point_entry = f"'POINT({point})'"
                # the id was transferring as a float so this is just to remove decimal
                row_values = process_values(row)
                # this was tough - everything needs to be a string and text being inserted wrapped in '' including wkt
                try:
                    # cursor.execute(f"INSERT INTO parcels ({', '.join(cols)}, geom, geom_c) VALUES ({', '.join(row_values)}, ST_GeometryFromText('MULTIPOLYGON({parcel})', 4326), {point_entry})")
                    cursor.execute(f"INSERT INTO parcels ({', '.join(cols)}, parcel_area, geom, geom_c) VALUES ({', '.join(row_values)}, ST_Area('SRID=4326;MULTIPOLYGON({parcel})'::geometry), 'MULTIPOLYGON({parcel})', {point_entry})")
                except:
                    d = 1
            connection.commit()
        cursor.execute("CREATE INDEX idx_parcels_geom ON parcels USING GIST (geom)")
        cursor.execute("CREATE INDEX idx_parcels_geom_c ON parcels USING GIST (geom_c)")
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def populate_elections():
    files = [file for file in Path("../../data/shp_bdry_electionresults_2012_2020").glob("*4326.shp") if "Points" not in file.name]
    connection = psycopg2.connect(f"dbname=postgres user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
    cursor = connection.cursor()
    try:
        parsed_columns = set()
        for file in files:
            print(f"\nProcessing parcels from {file.name}")
            data = fiona.open(file)
            parsed_columns.update(set(parse_columns(data.schema)))
        parsed_columns = sorted(list(parsed_columns))
        # consolidate duplicates to Integers
        split_cols = [[col.split(" ")[0], " ".join(col.split(" ")[1:])] for col in parsed_columns]
        d = pd.DataFrame(split_cols)
        def cast_value(df):
            if df.shape[0] > 1:
                try:
                    return df.loc[df.iloc[:,1] == "INTEGER"]
                except:
                    pass
            return df
        f = d.groupby(0).apply(cast_value)
        parsed_columns = [" ".join(row) for row in f.values.tolist()]
        columns = ",".join(["id SERIAL", "year INTEGER"] + parsed_columns)
        cursor.execute(f"DROP TABLE IF EXISTS election")
        cursor.execute(f"""
            CREATE TABLE election (
                {columns},
                parcel_area DOUBLE PRECISION,
                geom GEOGRAPHY(MULTIPOLYGON),
                geom_c GEOGRAPHY(Point),

                PRIMARY KEY (id))
        """)

        # cursor.execute("""
        #     SELECT AddGeometryColumn('parcels', 'geom', 4326, 'MULTIPOLYGON', 2)
        # """)

        # cursor.execute("""
        #     SELECT AddGeometryColumn('parcels', 'geom_c', 4326, 'POINT', 2)
        # """)
        process_values = values_factory(parsed_columns)
        files = sorted(files, key=lambda x: re.findall("(20[0-9]{2,})", x.name)[0])
        years = []
        for n, file in enumerate(files):
            data = fiona.open(file)
            year = int(re.findall("(20[0-9]{2,})", file.name)[0])
            years.append(year)
            cursor.execute(f"ALTER TABLE parcels DROP COLUMN IF EXISTS vtdid_{year}")
            cursor.execute(f"ALTER TABLE parcels ADD COLUMN vtdid_{year} VARCHAR")
            # use arcpy to get attribute data, populate PostGIS using psycopg2
            cols = [col.split()[0] for col in parsed_columns]
            print(f"\nProcessing parcels from {file.name}")
            for n, row in tqdm(enumerate(data), total=len(data)):
                if row["geometry"]["type"] == "MultiPolygon":
                    parcel = ",".join([convert_polygon(shape) for shape in row["geometry"]["coordinates"]])
                else:
                    parcel = convert_polygon(row["geometry"]["coordinates"])
                if row["properties"]["LONGITUDE"] == float("inf"):
                    point_entry = "NULL"
                else:
                    point = str(row["properties"]["LONGITUDE"]) + " " + str(row["properties"]["LATITUDE"])
                    # point_entry = f"ST_GeometryFromText('POINT({point})', 4326)"
                    point_entry = f"'POINT({point})'"
                # the id was transferring as a float so this is just to remove decimal
                row_values = [str(year), *process_values(row)]
                # this was tough - everything needs to be a string and text being inserted wrapped in '' including wkt
                # cursor.execute(f"INSERT INTO parcels ({', '.join(cols)}, geom, geom_c) VALUES ({', '.join(row_values)}, ST_GeometryFromText('MULTIPOLYGON({parcel})', 4326), {point_entry})")
                cursor.execute(f"INSERT INTO election (year, {', '.join(cols)}, parcel_area, geom, geom_c) VALUES ({', '.join(row_values)}, ST_Area('SRID=4326;MULTIPOLYGON({parcel})'::geometry), 'MULTIPOLYGON({parcel})', {point_entry})")
                cursor.execute(f"UPDATE parcels SET vtdid_{year} = {row['properties']['VTDID' if year != 2012 else 'VTD']} WHERE ST_Intersects('SRID=4326;MULTIPOLYGON({parcel})'::geometry, parcels.geom_c::geometry)")
            connection.commit()
        cursor.execute("CREATE INDEX idx_election_geom ON election USING GIST (geom)")
        cursor.execute("CREATE INDEX idx_election_geom_c ON election USING GIST (geom_c)")
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

def populate_counties():
    file = Path("../../data/MetroCounties.json")
    with file.open("r") as f:
        data = json.load(f)

    def process_county_cols(row):
        columns = []
        for name, value in row["properties"].items():
            if isinstance(value, str):
                val_type = "VARCHAR"
            elif isinstance(value, float):
                val_type = "DOUBLE PRECISION"
            elif isinstance(value, int):
                val_type = "INTEGER"
        columns.append(f"{name} {val_type}")
        return columns
        

    parsed_columns = process_county_cols(data["features"][0])
    columns = ", ".join(["id SERIAL"] + parsed_columns)
    connection = psycopg2.connect(f"dbname=postgres user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
    cursor = connection.cursor()
    cursor.execute("drop table if exists counties")
    cursor.execute(f"""
        create table counties (
            {columns},
            geom GEOGRAPHY(POLYGON),

            primary key (id))
    """)

    def process_values(row):
        values = []
        for col in parsed_columns:
            value = row["properties"][col.split()[0]]
            if value is None:
                values.append("NULL")
            elif "VARCHAR" in col:
                value = value.replace("'", "")
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        return values

    cols = [col.split()[0] for col in parsed_columns]
    for row in data["features"]:
        parcel = convert_polygon(row["geometry"]["coordinates"])
        # the id was transferring as a float so this is just to remove decimal
        row_values = process_values(row)
        # this was tough - everything needs to be a string and text being inserted wrapped in '' including wkt
        try:
            cursor.execute(f"INSERT INTO counties ({', '.join(cols)}, geom) VALUES ({', '.join(row_values)}, 'POLYGON{parcel}')")
        except:
            d = 1
    cursor.execute("CREATE INDEX idx_counties_geom ON counties USING GIST (geom)")
    connection.commit()
    cursor.close()
    connection.close()

def populate_grid():
    import geopandas as gpd
    import numpy as np
    from shapely import wkt
    import pandas as pd
    from shapely.ops import cascaded_union

   
    def create_pnt(lng, lat):
        return f"{lng} {lat}"

    def create_WKT_grid(lng_lines: np.ndarray, lat_lines: np.ndarray):
        polygons = []
        for i_x in range(1, lng_lines.shape[0]):
            for i_y in range(1, lat_lines.shape[0]):
                ul = create_pnt(lng_lines[i_x - 1], lat_lines[i_y - 1])
                ur = create_pnt(lng_lines[i_x], lat_lines[i_y - 1])
                ll = create_pnt(lng_lines[i_x - 1], lat_lines[i_y])
                lr = create_pnt(lng_lines[i_x], lat_lines[i_y])
                points = ", ".join([ul, ur, lr, ll, ul])
                polygons.append(f"POLYGON(({points}))")
        return polygons

    file = Path("../../data/shp_bdry_counties_in_minnesota/mn_county_boundaries_500.shp")
    data = gpd.read_file(file)
    reprojected = data.to_crs("EPSG:4326")
    counties = ["Anoka", "Carver", "Dakota", "Hennepin", "Ramsey", "Scott", "Washington"]
    county_mask = reprojected["CTY_NAME"].isin(counties)
    county_data = reprojected.loc[county_mask]
    bounds = county_data.total_bounds
    x_grid = np.linspace(bounds[0], bounds[2], 60)
    y_grid = np.linspace(bounds[1], bounds[3], 60)

    polygons = create_WKT_grid(x_grid, y_grid)
    d = pd.Series(polygons).apply(wkt.loads)
    grid = gpd.GeoSeries(d)
    tc_metro = cascaded_union(county_data.geometry)
    metro_grids = grid.loc[grid.geometry.apply(lambda x: tc_metro.contains(x))]
    recs = metro_grids.geometry.astype(str).values.tolist()
    
    connection = None
    try:
        connection = psycopg2.connect(f"dbname=postgres user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
        cursor = connection.cursor()
        exist_check = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'parcels'
        )""" 
        cursor.execute(exist_check)
        table_exists = cursor.fetchone()
        if table_exists:
            cursor.execute("DROP TABLE IF EXISTS grids")
            cursor.execute(f"""
                CREATE TABLE grids (
                    id SERIAL,
                    grid_id INTEGER,
                    geom GEOGRAPHY(POLYGON),

                    primary key (id))
            """)

            cursor.execute("ALTER TABLE parcels DROP COLUMN IF EXISTS grid_id")
            cursor.execute("ALTER TABLE parcels ADD COLUMN grid_id INTEGER")

            print("\nProcessing grids")
            for n, rec in tqdm(enumerate(recs), total=len(recs)):
                rec = rec.replace("N (", "N(")
                # polygon = f"'SRID=4326;{rec}'::geography"
                cursor.execute(f"INSERT INTO grids (grid_id, geom) VALUES ({n}, '{rec}')")
                cursor.execute(f"UPDATE parcels SET grid_id = {n} WHERE ST_Within(geom_c::geometry, 'SRID=4326;{rec}'::geometry)")
                if n % 100:
                    connection.commit()
            connection.commit()
        cursor.execute("CREATE INDEX idx_grids_geom ON grids USING GIST (geom)")
        connection.commit()
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return

def populate_precincts():
    from shapely import wkt
    from shapely.ops import cascaded_union
    import geopandas as gpd
    connection = None
    try:
        connection = psycopg2.connect(f"dbname=postgres user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
        cursor = connection.cursor()
        exist_check = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'parcels'
        )""" 
        cursor.execute(exist_check)
        table_exists = cursor.fetchone()
        cursor.execute("DROP TABLE IF EXISTS districts")
        data = fiona.open(Path("../../data/shp_bdry_votingdistricts/bdry_votingdistricts_4326.shp"))
        parsed_columns = parse_columns(data.schema)
        columns = ",".join(["id SERIAL"] + parsed_columns)
        connection = psycopg2.connect(f"dbname=postgres user=postgres password='{os.getenv('POSTGRES_PASSWORD')}' host='localhost'")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS districts")
        cursor.execute(f"""
            CREATE TABLE districts (
                {columns},
                parcel_area DOUBLE PRECISION,
                geom GEOGRAPHY(POLYGON),
                geom_c GEOGRAPHY(Point),

                PRIMARY KEY (id))
        """)

        def process_values(row):
            values = []
            for col in parsed_columns:
                value = row["properties"][col.split()[0]]
                if value is None:
                    values.append("NULL")
                elif "VARCHAR" in col:
                    value = value.replace("'", "")
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))
            return values

        print("\nPopulating voting districts.")
        cols = [col.split()[0] for col in parsed_columns]
        for row in tqdm(data):
            parcel = convert_polygon(row["geometry"]["coordinates"])
            if row["properties"]["LONGITUDE"] == float("inf"):
                point_entry = "NULL"
            else:
                point = str(row["properties"]["LONGITUDE"]) + " " + str(row["properties"]["LATITUDE"])
                # point_entry = f"ST_GeometryFromText('POINT({point})', 4326)"
                point_entry = f"'POINT({point})'"
            # the id was transferring as a float so this is just to remove decimal
            row_values = process_values(row)
            # this was tough - everything needs to be a string and text being inserted wrapped in '' including wkt
            # cursor.execute(f"INSERT INTO parcels ({', '.join(cols)}, geom, geom_c) VALUES ({', '.join(row_values)}, ST_GeometryFromText('MULTIPOLYGON({parcel})', 4326), {point_entry})")
            cursor.execute(f"INSERT INTO districts ({', '.join(cols)}, parcel_area, geom, geom_c) VALUES ({', '.join(row_values)}, ST_Area('SRID=4326;MULTIPOLYGON({parcel})'::geometry), 'MULTIPOLYGON({parcel})', {point_entry})")
        connection.commit()
        if table_exists:
            df = gpd.read_file("../../data/shp_bdry_votingdistricts/bdry_votingdistricts_4326.shp")

            file = Path("../../data/shp_bdry_counties_in_minnesota/mn_county_boundaries_500.shp")
            data = gpd.read_file(file)
            reprojected = data.to_crs("EPSG:4326")
            counties = ["Anoka", "Carver", "Dakota", "Hennepin", "Ramsey", "Scott", "Washington"]
            county_mask = reprojected["CTY_NAME"].isin(counties)
            county_data = reprojected.loc[county_mask]
            tc_metro = cascaded_union(county_data.geometry)
            points = tc_metro.bounds
            bounds_polygon = f"POLYGON(({points[0]} {points[1]}, {points[0]} {points[3]}, {points[2]} {points[3]}, {points[2]} {points[1]}, {points[0]} {points[1]}))"
            bounds_polygon = wkt.loads(bounds_polygon)
            metro_districts = df.loc[df.geometry.apply(lambda x: bounds_polygon.contains(x))]
            recs = metro_districts[["PCTCODE", "geometry"]].astype(str).values.tolist()
            
            cursor.execute("ALTER TABLE parcels DROP COLUMN IF EXISTS pctcode")
            cursor.execute("ALTER TABLE parcels ADD COLUMN pctcode VARCHAR")

            print("\nProcessing districts in parcels table")
            for n, rec in tqdm(recs):
                rec = rec.replace("N (", "N(")
                cursor.execute(f"UPDATE parcels SET pctcode = '{n}' WHERE ST_Within(geom_c::geometry, 'SRID=4326;{rec}'::geometry)")
            connection.commit()
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", nargs='*', type=str, help="Types of files to process 'parcels' or 'counties'.")
    args = parser.parse_args()
    ops = []
    for arg in args.type:
        if arg == "parcels":
            ops.append(populate_parcels)
        elif arg == "counties":
            ops.append(populate_counties)
        elif arg == "grid":
            ops.append(populate_grid)
        elif arg == "districts":
            ops.append(populate_elections)
        elif arg == "all":
            ops.append(populate_parcels)
            ops.append(populate_elections)
            ops.append(populate_counties)
            ops.append(populate_grid)
            break
            # populate_precincts()
    
    [op() for op in ops]

