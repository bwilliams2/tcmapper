from django.shortcuts import render
from django.conf import settings
from geotools.election import all_election_data
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pathlib import Path
import uuid
import json

from geotools.path_calc import weighted_parcel_address_search
from geotools.misc import get_metro_counties
from geotools.stats import growth_rates

# Registers session cookie and gives template
def index(request):
    user_id = uuid.uuid4().hex
    request.session["user_uuid"] = user_id
    
    return render(
        request,
        "index.html"
    )

@api_view(["GET"])
def metro_counties(request):
    return Response({"counties": json.dumps(get_metro_counties())})


@api_view(["GET"])
def weight_search(request):
    longitude = float(request.query_params.get("longitude"))
    latitude = float(request.query_params.get("latitude"))
    radius = float(request.query_params.get("radius"))
    counties = get_metro_counties()
    address_data, features = weighted_parcel_address_search(longitude, latitude, radius)
    growth_data = growth_rates(address_data)
    address_data = address_data.loc[address_data["YEAR_BUILT"] != 0]
    use_classes = address_data["USECLASS1"].unique().tolist()
    # location_data = address_data[["LATITUDE", "LONGITUDE", "WEIGHT"]].values.tolist()
    location_data = address_data[["LATITUDE", "LONGITUDE", "YEAR_BUILT"]].rename(columns={"YEAR_BUILT": "WEIGHT"}).values.tolist()
    histogram_data = address_data.groupby(["YEAR_BUILT", "USECLASS1"]).size()
    histogram_data.name = "COUNT"
    histogram_data = histogram_data.unstack().reset_index().fillna(0).to_dict("records")
    address_raw = address_data.groupby(["YEAR_BUILT"]).size()
    address_raw.name = "COUNT"
    address_raw = address_raw.to_dict()
    address_weight = address_data.groupby("YEAR_BUILT")["WEIGHT"].sum().reset_index().to_dict(orient="records")
    return_obj = {
        "locationData": json.dumps(location_data),
        "histData": json.dumps(histogram_data),
        "growthData": json.dumps(growth_data),
        "yearData": json.dumps(address_raw),
        "weightData": json.dumps(address_weight),
        "features": json.dumps(features),
        "useClasses": json.dumps(use_classes),
        "counties": json.dumps(counties),
    }
    return Response(return_obj)


@api_view(["GET"])
def all_election_precincts(request):
    year = request.query_params.get("year")
    data, features = all_election_data(year)
    data = data.dropna(how="all", axis=1).sort_index(axis=1)
    cols = data.columns.tolist()

    voting = {}
    used_cols = []
    for col in cols:
        if "us" in col or "mn" in col:
            base = col[:5] if "mnag" not in col else col[:4]
            if base not in voting:
                voting[base] = [col]
            else:
                voting[base].append(col)
            used_cols.append(col)
        elif "2016" in col:
            if "usprs" in voting:
                voting["usprs"].append(col)
            else:
                voting["usprs"] = [col]
            used_cols.append(col)
    
    election_info = ["ab_mb", "edr", "reg7am", "regmilovab", "signatures", "tabmodel", "tabsystem", "totvoting", "mailballot"]
    voting["election"] = [item for item in election_info if item in cols]
    precinct_stats = ["mean_age", "median_age", "mean_emv", "median_emv", "growth"]
    voting["precinct"] = [item for item in precinct_stats if item in cols]
    records = data.where(data.notna(), None).to_dict(orient="records")
    return Response({"selection": json.dumps(voting), "data": json.dumps(records), "features": json.dumps(features)})