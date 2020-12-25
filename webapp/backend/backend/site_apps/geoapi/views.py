from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pathlib import Path
import uuid
import json

from geotools.path_calc import weighted_parcel_address_search

# Registers session cookie and gives template
def index(request):
    user_id = uuid.uuid4().hex
    request.session["user_uuid"] = user_id
    
    return render(
        request,
        "index.html"
    )

@api_view(["GET"])
def weight_search(request):
    longitude = float(request.query_params.get("longitude"))
    latitude = float(request.query_params.get("latitude"))
    radius = float(request.query_params.get("radius"))
    address_data, features = weighted_parcel_address_search(longitude, latitude, radius)
    address_data = address_data.loc[address_data["YEAR_BUILT"] != 0]
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
        "yearData": json.dumps(address_raw),
        "weightData": json.dumps(address_weight),
        "features": json.dumps(features),
    }
    return Response(return_obj)
