from pathlib import Path
import geopandas as gpd
import sys
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [FILE]",
        description="Consolidate county shapefile into metro counties."
    )
    parser.add_argument('file', nargs='1')
    return parser

def main(file: Path):
    data = gpd.read_file(file)
    reprojected = data.to_crs("EPSG:4326")
    counties = ["Anoka", "Carver", "Dakota", "Hennepin", "Ramsey", "Scott", "Washington"]
    county_mask = reprojected["CTY_NAME"].isin(counties)
    new_file = file.parent.joinpath(file.stem + "_4326.json")
    reprojected.loc[county_mask].to_file(new_file, driver="GeoJSON")
    return

if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    main(Path(args.file))