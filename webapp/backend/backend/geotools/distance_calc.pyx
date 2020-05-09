import numpy as np

cdef extern from "../../../../tools/cShapeTools/include/PathFinder/process.h":

    void geoSearch(char * fname, double baseLong, double baseLat, int searchRadius, double * distances)

def getDistances(bytes fname, double baseLong, double baseLat, int searchRadius, int recordLength):
    distances_array = np.empty((recordLength * 2), np.doublec)
    cdef double[:] distances = distances_array
    cdef char * cfname = fname
    geoSearch(cfname, baseLong, baseLat, searchRadius, &distances[0])
    return distances_array