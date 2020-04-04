#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include <shapefil.h>
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

int main ( int argc, char *argv[], double longitude, double latitude, double distance)
{
    int i;
    DBFHandle dbfH = DBFOpen( argv[1], "r" );
    int records = DBFGetRecordCount(dbfH);
    PJ_COORD other = proj_coord (latitude, longitude, 0, 0);
    double (*distances) = malloc (sizeof(double) * records * 3);
    geoSearch(dbfH, latitude, longitude, distance, distances);
    DBFClose(dbfH);
    free(distances);
    return 0;
}
