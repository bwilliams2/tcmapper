#include <stdio.h>
#ifndef _PROCESS_H_
#define _PROCESS_H_

    void makeArray(double longlat[][2], int numrows, FILE *ifp);
    void geoConversion(double longlat_array[][2], int line_nums);
    void distanceCalc(double longlat_array[][2], double distance[], int line_nums, PJ_COORD base);
    void geoSearch(char * fname, double baseLong, double baseLat, int searchRadius, double * distances);

#endif