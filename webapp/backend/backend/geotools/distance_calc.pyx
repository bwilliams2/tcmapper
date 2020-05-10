import numpy as np
cimport numpy as np


cdef extern from "/home/bryce/code/commute/tools/cShapeTools/include/PathFinder/process.c":
    void geoSearch(char * fname, double baseLong, double baseLat, int searchRadius, double * distances)

cpdef get_distances(bytes fname, double baseLong, double baseLat, int searchRadius, int recordLength):
    distances_array = np.ascontiguousarray(np.zeros((recordLength, dtype=np.double) - 1.)
    cdef double[::1] distances = distances_array
    cdef char * cfname = fname
    geoSearch(cfname, baseLong, baseLat, searchRadius, &distances[0])
    return distances_array