from pathlib import Path
import subprocess
import multiprocessing
import argparse



# Add long-lat to dbf file
def process_file(fpath):
    subprocess.run(["ShapeFileFixer", str(fpath.absolute())], capture_output=True)
    new_file = str(fpath.absolute().parent.joinpath(f"{fpath.stem}_4326{fpath.suffix}"))
    ogr_out = subprocess.run(["ogr2ogr", "-s_srs", "EPSG:26915", "-t_srs", "EPSG:4326", new_file, str(fpath.absolute())])
    return ogr_out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Types of files to process 'parcels' or 'counties'.")
    args = parser.parse_args()
    if args.path is None:
        parcel_dir = Path("../../data/shp_plan_regional_parcels")
    else:
        parcel_dir = Path(args.path)
        if not parcel_dir.exists():
            raise ValueError("Provide path does not exist!")
    parcel_files = list(parcel_dir.glob("*.shp"))
    pool = multiprocessing.Pool(processes=6)
    res = pool.map(process_file, parcel_files)
    pool.close()