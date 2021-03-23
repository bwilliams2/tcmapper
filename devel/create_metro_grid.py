import shapely.geometry
import multiprocessing as mp
import time
import pyproj
import math
import numpy as np
from tqdm import tqdm
from pathlib import Path
from geotools.path_calc import address_search, get_metro_bounds

def worker(x, transformed_sw, transformed_ne, stepsize, q):
    # Set up projections
    p_ll = pyproj.Proj(init='epsg:4326')
    p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913
    grindpoints = []
    for y in np.arange(transformed_sw[1], transformed_ne[1], stepsize):
        p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
        # gridpoints.append(p)
        q.put(p)
    return

def listener(q):
    out_file = Path("metro_grid.csv")
    with out_file.open("w") as f:
        f.write('lon;lat\n')
        while 1:
            m = q.get()
            if m == "kill":
                break
            f.write('{:f};{:f}\n'.format(m.x, m.y))
            f.flush()


def main():
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(mp.cpu_count() + 2)

    #put listener to work first
    watcher = pool.apply_async(listener, (q,))

    # Set up projections
    p_ll = pyproj.Proj(init='epsg:4326')
    p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

    bounds = get_metro_bounds()
    # Create corners of rectangle to be transformed to a grid
    sw = shapely.geometry.Point((bounds[0,0], bounds[0,1]))
    ne = shapely.geometry.Point((bounds[1,0], bounds[1,1]))

    stepsize = 1000 # 1 km grid step size

    # Project corners to target projection
    transformed_sw = pyproj.transform(p_ll, p_mt, sw.x, sw.y) # Transform NW point to 3857
    transformed_ne = pyproj.transform(p_ll, p_mt, ne.x, ne.y) # .. same for SE

    # # Iterate over 2D area
    # out_file = Path("metro_grid.csv")
    # gridpoints = []
    # x = transformed_sw[0]
    # for x in tqdm(np.arange(transformed_sw[0], transformed_ne[0], stepsize), desc="x steps"):
    #     for y in tqdm(np.arange(transformed_sw[1], transformed_ne[1], stepsize), desc="y steps"):
    #         p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
    #         gridpoints.append(p)

    jobs = []
    for x in tqdm(np.arange(transformed_sw[0], transformed_ne[0], stepsize)):
    # for i in range(80):
        job = pool.apply_async(worker, (x, transformed_sw, transformed_ne, stepsize, q))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs: 
        job.get()

    #now we are done, kill the listener
    q.put('kill')
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()