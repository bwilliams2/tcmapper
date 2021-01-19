import json
from importlib.resources import path, contents

def get_metro_counties():
    with path("geotools", "data") as data_dir:
        file = data_dir.joinpath("MetroCounties.json")
        with file.open("r") as f:
            county_data = json.load(f)
    return county_data