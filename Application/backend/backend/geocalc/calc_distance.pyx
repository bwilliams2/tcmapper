# https://github.com/megaserg/geographiclib-cython-bindings/blob/master/geographiclib_cython.pyx
cimport cgeographiclib
cimport numpy as np
import numpy as np
import cython
from libcpp cimport bool as cbool



cdef class PyGeodesic:

    cdef const cgeographiclib.Geodesic* geodesic
    cdef cbool needs_delete

    def __cinit__(self, double radius=0.0):
        if radius == 0.0:
            self.geodesic = &(cgeographiclib.Geodesic.WGS84())
            self.needs_delete = False
        else:
            self.geodesic = new cgeographiclib.Geodesic(radius, 0.0)
            self.needs_delete = True

    def __dealloc__(self):
        if self.needs_delete:
            del self.geodesic

    cpdef Direct(self, double lat1, double lon1, double azi1, double s12):
        cdef double lat2 = 0.0, lon2 = 0.0, azi2 = 0.0
        self.geodesic.Direct(lat1, lon1, azi1, s12, lat2, lon2, azi2)
        return {
             'lat1': lat1, 'lon1': lon1,
             'lat2': lat2, 'lon2': lon2,
             's12': s12, 'azi1': azi1, 'azi2': azi2,
        }

    cdef double Inverse(self, double lat1, double lon1, double lat2, double lon2):
        cdef double s12 = 0.0, azi1 = 0.0, azi2 = 0.0
        self.geodesic.Inverse(lat1, lon1, lat2, lon2, s12, azi1, azi2)
        return s12

    cpdef InverseLine(self, double lat1, double lon1, double lat2, double lon2): 
        return PyGeodesicLine(lat1, lon1, lat2, lon2)

cdef class PyGeodesicLine:

    cdef cgeographiclib.GeodesicLine line
    cdef readonly double s13

    def __cinit__(self, double lat1, double lon1, double lat2, double lon2):
        self.line = cgeographiclib.Geodesic.WGS84().InverseLine(lat1, lon1, lat2, lon2)
        self.s13 = self.line.Distance()
    
    cpdef Position(self, double s12):
        cdef double lat2 = 0.0, lon2 = 0.0
        self.line.Position(s12, lat2, lon2)
        return {
            'lat2': lat2, 'lon2': lon2, 's12': s12
        }


# cdef double GeodesicInverse(double lat1, double lon1, double lat2, double lon2):
#     cdef double s12 = 0.0, azi1 = 0.0, azi2 = 0.0
#     geodesic = &(cgeographiclib.Geodesic.WGS84())
#     geodesic.Inverse(lat1, lon1, lat2, lon2, s12, azi1, azi2)
#     del geodesic
#     return s12

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
        distances[i] = PyGeodesic().Inverse(lat1, lon1, lat2, lon2)

    return distances_arr