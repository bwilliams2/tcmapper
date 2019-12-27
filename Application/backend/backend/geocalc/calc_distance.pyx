# https://github.com/megaserg/geographiclib-cython-bindings/blob/master/geographiclib_cython.pyx
cimport cgeographiclib
cimport numpy as np
import numpy as np
import cython

cdef double GeodesicInverse(double lat1, double lon1, double lat2, double lon2):
    cdef double s12 = 0.0, azi1 = 0.0, azi2 = 0.0
    cdef const cgeographiclib.Geodesic* geodesic
    geodesic.Inverse(lat1, lon1, lat2, lon2, s12, azi1, azi2)
    return s12

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def FindDistances(double [:, :] locs, double lat1, double lon1):
    distances_arr = np.empty(locs.shape[0], dtype=np.double)
    cdef double lat2
    cdef double lon2
    cdef double[:] distances = distances_arr
    cdef int i

    for i in range(locs.shape[0]):
        lat2 = locs[i, 0]
        lon2 = locs[i, 1]
        distances[i] = GeodesicInverse(lat1, lon1, lat2, lon2)

    return distances_arr