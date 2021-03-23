import multiprocessing as mp
from geotools.weighting import weighting_function
from geotools.path_calc import address_search, get_metro_bounds
from pathlib import Path
import dataclasses
import pandas as pd
import numpy as np

@dataclasses.dataclass
class Weight:
    lon: float
    lat: float
    weight: float


def worker(row, q):
    address_data, features = address_search(row[0], row[1], 5000)
    if len(address_data) > 5:
        weights = np.sum(weighting_function(address_data))
        q.put(Weight(row[0], row[1], weights))

def listener(q):
    out_file = Path("weight_grid.csv")
    with out_file.open("w") as f:
        f.write("lat; lon; weight\n")
        while 1:
            m = q.get()
            if m == "kill":
                break
            f.write('{:f};{:f};{:f}\n'.format(m.x, m.y,m.weight))
            f.flush()


def main():
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(mp.cpu_count() + 2)

    #put listener to work first
    watcher = pool.apply_async(listener, (q,))
    with open("metro_grid.csv") as f:
        rows = pd.read_csv(f, sep=";").values

    jobs = []
    for row in rows:
    # for i in range(80):
        job = pool.apply_async(worker, (row, q))
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