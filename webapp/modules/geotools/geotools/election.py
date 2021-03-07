from pathlib import Path
import glob
from typing import Iterable

import fiona
import numpy as np
import os
import pandas as pd
import json

import psycopg2
import psycopg2.extras


dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

counties = ["Anoka", "Dakota", "Hennepin", "Scott", "Ramsey", "Washington", "Carver"]

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
    

def metro_ids(year: int, mean_emv: float = None, mean_age: float = None, city_dis: float = None):
    additional_query = []
    if mean_emv is not None:
        additional_query.append(f"mean_emv BETWEEN {mean_emv * 0.9} AND {mean_emv * 1.1}")
    if mean_age is not None:
        additional_query.append(f"mean_age BETWEEN {mean_age * 0.9} AND {mean_age * 1.1}")
    if city_dis is not None:
        additional_query.append(f"cit_dis BETWEEN {city_dis * 0.8} AND {city_dis * 1.2}")
    if len(additional_query) > 0:
        additional_query = " AND " + " AND ".join(additional_query)
    else:
        additional_query = ""


    # counties = [f"'{val}'" for val in counties]
    county_array = "'{" + f",".join(counties) + "}'::text[]"
    additional_query += f" AND (p.countyname = ANY ({county_array}))"

    try:
        connection = psycopg2.connect(f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"SELECT id FROM processed_election p WHERE p.year = {year}{additional_query}")
        d = cursor.fetchall()
        ids = [val["id"] for val in d]
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return ids

def precinct_stat_ranges():
    year = 2020
    counties = ["Anoka", "Dakota", "Hennepin", "Scott", "Ramsey", "Washington", "Carver"]
    # counties = [f"'{val}'" for val in counties]
    county_array = "'{" + f",".join(counties) + "}'::text[]"
    additional_query = f" AND (p.countyname = ANY ({county_array}))"

    try:
        connection = psycopg2.connect(f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"\
            SELECT "\
            f"MAX(p.mean_emv) as max_mean_emv, "\
            f"MIN(p.mean_emv) as min_mean_emv, "\
            f"MAX(p.mean_age) as max_mean_age, "\
            f"MIN(p.mean_age) as min_mean_age, "\
            f"MAX(p.cit_dis) as max_city_dis, "\
            f"MIN(p.cit_dis) as min_city_dis, "\
            f"MAX(p.usprs_vote_density) as max_usprs_vote_density, "\
            f"MIN(p.usprs_vote_density) as min_usprs_vote_density, "\
            f"MAX(p.growth) as max_growth, "\
            f"MIN(p.growth) as min_growth, "\
            f"MAX(p.medinc) as max_medinc, "\
            f"MIN(p.medinc) as min_medinc, "\
            f"MAX(p.medage) as max_medage, "\
            f"MIN(p.medage) as min_medage, "\
            f"MAX(p.ronehouse) as max_ronehouse, "\
            f"MIN(p.ronehouse) as min_ronehouse "\
            f"FROM processed_election p WHERE p.year = {year}{additional_query}")
        d = cursor.fetchall()[0]
        values = {}
        for cat in ["mean_age", "mean_emv", "city_dis", "growth", "usprs_vote_density", "medinc", "medage", "ronehouse"]:
            values[cat] = [d[f"min_{cat}"], d[f"max_{cat}"]]
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return values

def model_nearest_neighbors(n_neighbors: int = 10, year: int = 2020, **kwargs):
    # Create auto-centered array and find nearest neighbor
    select_query = "p." + ", p.".join(kwargs.keys())
    county_array = "'{" + f",".join(counties) + "}'::text[]"
    query = f"SELECT p.id, {select_query} FROM processed_election p WHERE p.year = {year} AND (p.countyname = ANY ({county_array}))"

    try:
        connection = psycopg2.connect(f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        d = cursor.fetchall()
    finally:
        if (connection):
            cursor.close()
            connection.close()
    center = np.array(list(kwargs.values()))
    df = pd.DataFrame(d).dropna()
    cols = [col for col in df.columns if col != "id"]
    records = df[cols].values
    records = np.vstack([records, center])
    d = (records - np.mean(records, axis=0)) / (np.max(records, axis=0) - np.min(records, axis=0))
    min_args = np.argsort(np.sum((d[:-1] - d[-1]) ** 2, axis=1))
    return df["id"].iloc[min_args[:n_neighbors]]
