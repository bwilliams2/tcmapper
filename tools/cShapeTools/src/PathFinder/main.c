#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include <string.h>
#include <shapefil.h>
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

int main ( int argc, char *argv[])
{
    int i;
    char **endptr;
    printf("%s\n", argv[1]);
    if(strcmp(argv[1], "--bounds") == 0) {
        printf("%s\n", argv[1]);
        double (*boxCoordinates) = malloc (sizeof(double) * 4);
        printf("%s", argv[2]);
        getBoundingBox(argv[2], boxCoordinates);
        for(i = 0; i < 4; i++) {
            printf("%lf ", boxCoordinates[i]);
        }
        free(boxCoordinates);
    } else if(argv[1] == "--distance") {
        DBFHandle dbfH = DBFOpen( argv[2], "r" );
        double longitude = strtod( argv[3], endptr );
        double latitude = strtod( argv[4], endptr );
        double distance = strtod( argv[5], endptr );

        int records = DBFGetRecordCount(dbfH);
        PJ_COORD other = proj_coord (latitude, longitude, 0, 0);
        double (*distances) = malloc (sizeof(double) * records * 3);
        printf("Longitude, Latitude %lf, %lf \n", longitude, latitude);
        printf("Distance %lf \n", distance);
        DBFClose(dbfH);
        geoSearch(argv[1], latitude, longitude, distance, distances);
        free(distances);
    }
    return 0;
}
