#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include <shapefil.h>
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

int main ( int argc, char *argv[])
{
    int i;
    char **endptr;
    DBFHandle dbfH = DBFOpen( argv[1], "r" );
    double longitude = strtod( argv[2], endptr );
    double latitude = strtod( argv[3], endptr );
    double distance = strtod( argv[4], endptr );

    int records = DBFGetRecordCount(dbfH);
    PJ_COORD other = proj_coord (latitude, longitude, 0, 0);
    double (*distances) = malloc (sizeof(double) * records * 3);
    printf("Longitude, Latitude %lf, %lf \n", longitude, latitude);
    printf("Distance %lf \n", distance);
    DBFClose(dbfH);
    geoSearch(argv[1], latitude, longitude, distance, distances);
    free(distances);
    return 0;
}
