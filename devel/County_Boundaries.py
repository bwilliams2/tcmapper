#%%
import fiona
from geopy.distance import geodesic
from pyproj import Proj, transform
import pandas as pd
from pathlib import Path
import numpy as np

file = Path("../data/shp_bdry_counties_in_minnesota/mn_county_boundaries_500.shp")
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
county_data = reprojected.loc[county_mask]
# %%
# reprojected.loc[county_mask].to_file("MetroCounties.json", driver="GeoJSON")

#%%
bounds = county_data.total_bounds
bounds
x_grid = np.linspace(bounds[0], bounds[2], 75)
y_grid = np.linspace(bounds[1], bounds[3], 75)
# %%
import matplotlib.pyplot as plt
ax = county_data.plot()
[xmin, xmax] = ax.get_xlim()
[ymin, ymax] = ax.get_ylim()
ax.hlines(y_grid, xmin, xmax)
ax.vlines(x_grid, ymin, ymax)
plt.show()

#%%
x_grid
#%% find grid points within counties
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

#%%
from shapely import wkt
polygons = create_WKT_grid(x_grid, y_grid)
d = pd.Series(polygons).apply(wkt.loads)
grid = gpd.GeoSeries(d)
f = gpd.GeoDataFrame({"geometry": grid, "grid": np.arange(0, len(polygons))}, crs=county_data.crs)

#%%
# Can't get overlay to work correctly so going to use shapely instead
overlay_grid = gpd.overlay(f, county_data, how="intersection")
overlay_grid.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 2) #Use your second dataframe

#%%
from shapely.ops import cascaded_union
tc_metro = cascaded_union(county_data.geometry)
metro_grids = grid.loc[grid.geometry.apply(lambda x: tc_metro.contains(x))]
metro_grids.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 2) #Use your second dataframe

#%%
recs = metro_grids.geometry.astype(str).values.tolist()

# %%
from geotools.search import polygon_search
d = polygon_search(recs[0])