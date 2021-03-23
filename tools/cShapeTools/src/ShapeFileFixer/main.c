#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <proj.h>
#include <shapefil.h>
#include "../../include/ShapeFileFixer/shpgeo.h"
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

// Adds long lat to DBF file
// long lat not in DBF for metro data set
void alterLongLat(char fpath[]) {
    printf("%s\n", fpath);
    DBFHandle dbfH = DBFOpen(fpath, "rb+");
    SHPHandle shpH = SHPOpen(fpath, "rb+");
    
    double currLong, currLat, newLong, newLat;
    int i;

    
    PJ_CONTEXT *C;
    PJ *P;
    PJ* P_for_GIS;
    PJ_COORD a, b;
    PT  Centrd; 
    
    C = proj_context_create();

    P = proj_create_crs_to_crs (C,
                                "EPSG:26915",
                                "EPSG:4326",
                                NULL);

    if (0==P) {
        fprintf(stderr, "Oops\n");
        // return 1;
    }

    /* This will ensure that the order of coordinates for the input CRS */
    /* will be longitude, latitude, whereas EPSG:4326 mandates latitude, */
    /* longitude */
    // P_for_GIS = proj_normalize_for_visualization(C, P);
    // if( 0 == P_for_GIS )  {
    //     fprintf(stderr, "Oops\n");
    //     // return 1;
    // }
    // proj_destroy(P);
    // P = P_for_GIS;


    int records = DBFGetRecordCount(dbfH);
    int hasChanged = 0;
    int longLoc = DBFGetFieldIndex(dbfH, "LONGITUDE");
    printf("%d\n", longLoc);
    if (longLoc == -1)
    {
        DBFAddField(dbfH, "LONGITUDE", FTDouble, 11, 7);
        longLoc = DBFGetFieldIndex(dbfH, "LONGITUDE");
        hasChanged = 1;
    }
    int latLoc = DBFGetFieldIndex(dbfH, "LATITUDE");
    printf("%d\n", latLoc);
    if (latLoc == -1)
    {
        DBFAddField(dbfH, "LATITUDE", FTDouble, 11, 7);
        latLoc = DBFGetFieldIndex(dbfH, "LATITUDE");
        hasChanged = 1;
    }
    // if (hasChanged)
    // {
    DBFClose(dbfH);
    DBFHandle dbfHW = DBFOpen(fpath, "rb+");
    for (i = 0; i < records; ++i) {
        SHPObject *currRecord = SHPReadObject(shpH, i);
        printf("\n");
        printf("Vertices: %d\n", currRecord -> nVertices);
        printf("x: %lf\n", currRecord->dfXMin);
        printf("y: %lf\n", currRecord->dfYMin);

        Centrd = SHPCentrd_2d ( currRecord ); 

        if (currRecord -> nVertices == 1) {
            currLong = currRecord->dfXMin;
            currLat = currRecord->dfYMin;
        } else {
            currLong = Centrd.x;
            currLat = Centrd.y;
        }

        SHPDestroyObject(currRecord);
        printf("Longitude: %lf Latitude: %lf\n", currLong, currLat);

        a = proj_coord (currLong, currLat, 0, 0);
        b = proj_trans (P, PJ_FWD, a);
        newLong = roundf(b.lp.phi*10000000) / 10000000;
        newLat = roundf(b.lp.lam*10000000) / 10000000;
        printf("Longitude: %lf Latitude: %lf\n", newLong, newLat);
        DBFWriteDoubleAttribute(dbfHW, i, longLoc, newLong);
        DBFWriteDoubleAttribute(dbfHW, i, latLoc, newLat);
    }
    // }

    /* Clean up */
    proj_destroy (P);
    proj_context_destroy (C); /* may be omitted in the single threaded case */
    DBFClose(dbfHW);
    SHPClose(shpH);
}


int main ( int argc, char *argv[] )
{
    alterLongLat(argv[1]);
    return 0;
}