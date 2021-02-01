import numpy as np
cimport numpy as np


cdef extern from "../../../../tools/cShapeTools/include/PathFinder/process.c":
    void geoSearch(char * fname, double baseLong, double baseLat, int searchRadius, double * distances)
    void getBoundingBox(char * fname, double * boxCoordinates)

cpdef get_distances(bytes fname, double baseLong, double baseLat, int searchRadius, int recordLength):
    distances_array = np.ascontiguousarray(np.zeros(recordLength, dtype=np.double) - 1.)
    cdef double[::1] distances = distances_array
    cdef char * cfname = fname
    geoSearch(cfname, baseLong, baseLat, searchRadius, &distances[0])
    return distances_array

cpdef get_bounding_box(bytes fname):
    box_coordinates_array = np.ascontiguousarray(np.zeros(4))
    cdef double[::1] box_coordinates = box_coordinates_array
    cdef char * cfname = fname
    getBoundingBox(cfname, &box_coordinates[0])
    return box_coordinates_array
