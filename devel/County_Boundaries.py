#%%
import fiona
from geopy.distance import geodesic
from pyproj import Proj, transform
import pandas as pd
from pathlib import Path
import numpy as np

file = Path("../webapp/modules/geotools/geotools/data/shp_bdry_counties_in_minnesota/mn_county_boundaries_500.shp")
fpath = str(file.absolute())
datapoint = fiona.open(fpath)
print(file.name)

print(f"Points file: {len(datapoint)}")
data = fiona.open(fpath.replace("Points", ""))
print(f"Parcel file: {len(data)}")
print("\n")

#%%
import geopandas as gpd
data = gpd.read_file(file)
data
# %%
data.plot()
# %%
data.crs
# %%
reprojected = data.to_crs("EPSG:4326")

# %%
reprojected.plot()

#%%
counties = ["Anoka", "Carver", "Dakota", "Hennepin", "Ramsey", "Scott", "Washington"]
county_mask = reprojected["CTY_NAME"].isin(counties)
reprojected.loc[county_mask].plot()
# %%
reprojected.loc[county_mask].to_file("MetroCounties.json", driver="GeoJSON")
# %%
