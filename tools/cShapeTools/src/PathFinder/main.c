#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include <shapefil.h>
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

int main ( int argc, char *argv[] )
{
    int i;
    DBFHandle dbfH = DBFOpen( argv[1], "r" );
    int records = DBFGetRecordCount(dbfH);
    PJ_COORD other = proj_coord (43.1, -93.1, 0, 0);
    double (*distances) = malloc (sizeof(double)*records);
    geoSearch(dbfH, 45.147901, -93.134040, 5000, distances);
    DBFClose(dbfH);
    free(distances);
    return 0;
}
