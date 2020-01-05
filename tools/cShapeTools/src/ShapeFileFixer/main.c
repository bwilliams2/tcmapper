#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include <shapefil.h>
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

void alterLongLat(DBFHandle dbfH, SHPHandle shpH) {
    double currLong, currLat, newLong, newLat;
    int i;

    
    PJ_CONTEXT *C;
    PJ *P;
    PJ* P_for_GIS;
    PJ_COORD a, b;
    
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

    int longLoc = DBFGetFieldIndex(dbfH, "LONGITUDE");
    if (longLoc == -1)
    {
        DBFAddField(dbfH, "LONGITUDE", FTDouble, 7, 6);
        int longLoc = DBFGetFieldIndex(dbfH, "LONGITUDE");
    }
    int latLoc = DBFGetFieldIndex(dbfH, "LATITUDE");
    if (latLoc == -1)
    {
        DBFAddField(dbfH, "LATITUDE", FTDouble, 7, 6);
        int latLoc = DBFGetFieldIndex(dbfH, "LATITUDE");
    }
    for (i = 0; i < records; ++i) {
        SHPObject *currRecord = SHPReadObject(shpH, i);
        printf("\n");
        printf("Vertices: %d\n", currRecord -> nVertices);
        printf("x: %lf\n", currRecord->dfXMin);
        printf("y: %lf\n", currRecord->dfYMin);
        currLong = currRecord->dfXMin;
        currLat = currRecord->dfYMin;
        // printf("Longitude: %lf Latitude: %lf\n", currLong, currLat);
        SHPDestroyObject(currRecord);
        // if (currLong > 0) {
        a = proj_coord (currLong, currLat, 0, 0);
        b = proj_trans (P, PJ_FWD, a);
        newLong = b.lp.phi;
        newLat = b.lp.lam;
        printf("Longitude: %lf Latitude: %lf\n", newLong, newLat);
        DBFWriteDoubleAttribute(dbfH, i, longLoc, newLong);
        DBFWriteDoubleAttribute(dbfH, i, latLoc, newLat);
        // } 
    }

    /* Clean up */
    proj_destroy (P);
    proj_context_destroy (C); /* may be omitted in the single threaded case */
}

int main ( int argc, char *argv[] )
{
    DBFHandle dbfH = DBFOpen(argv[1], "rb+");
    SHPHandle shpH = SHPOpen(argv[1], "rb+");
    alterLongLat(dbfH, shpH);
    DBFClose(dbfH);
    SHPClose(shpH);
    return 0;
}