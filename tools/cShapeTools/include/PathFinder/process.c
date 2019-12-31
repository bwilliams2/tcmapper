#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include <shapefil.h>
#include <geodesic.h>
#include "./process.h"

void geoSearch(DBFHandle dbfH, double baseLat, double baseLong, int searchRadius, double * distances) 
{
    PJ_CONTEXT *C;
    PJ *P;
    PJ* P_for_GIS;
    PJ_COORD other;
    double otherLong, otherLat, distance;
    struct geod_geodesic g;
    double s12;

    int i;
    int n = 0;
    int records = DBFGetRecordCount(dbfH);
    int longLoc = DBFGetFieldIndex(dbfH, "LONGITUDE");
    int latLoc = DBFGetFieldIndex(dbfH, "LATITUDE");
    int effDateLoc = DBFGetFieldIndex(dbfH, "EFF_DATE");
    
    geod_init(&g, 6378137, 1/298.257223563);
    for (i = 0; i < records; ++i) {
        otherLong = DBFReadDoubleAttribute(dbfH, i, longLoc);
        otherLat = DBFReadDoubleAttribute(dbfH, i, latLoc);
        geod_inverse(&g, otherLat, otherLong, baseLat, baseLong, &distance, 0, 0);
        distances[i] = distance;
        if (distance <= searchRadius) {
            printf("\n");
            printf("This distance is %lf km\n", distance / 1000);
            const char *effDate = DBFReadStringAttribute(dbfH, i, effDateLoc);
            printf("Effective Date: %s", effDate);
            ++n;
        }
    }
    printf("Number of addresses within %d m is %d\n", searchRadius, n);
}

void geoConversion(double longlat_array[][2], int line_nums) {
    PJ_CONTEXT *C;
    PJ *P;
    PJ* P_for_GIS;
    PJ_COORD a, b;
    int i;
    double distance;

    /* or you may set C=PJ_DEFAULT_CTX if you are sure you will     */
    /* use PJ objects from only one thread                          */
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
    P_for_GIS = proj_normalize_for_visualization(C, P);
    if( 0 == P_for_GIS )  {
        fprintf(stderr, "Oops\n");
        // return 1;
    }
    proj_destroy(P);
    P = P_for_GIS;

    /* a coordinate union representing Copenhagen: 55d N, 12d E    */
    /* Given that we have used proj_normalize_for_visualization(), the order of
    /* coordinates is longitude, latitude, and values are expressed in degrees. */
    for (i=0; i < line_nums; ++i) {
        a = proj_coord (longlat_array[i][0], longlat_array[i][1], 0, 0);

        /* transform to UTM zone 32, then back to geographical */
        b = proj_trans (P, PJ_FWD, a);
        longlat_array[i][0] = b.lp.phi;
        longlat_array[i][1] = b.lp.lam;
        printf ("longitude: %g, latitude: %g\n", b.lp.lam, b.lp.phi);
        // b = proj_trans (P, PJ_INV, b);
        // printf ("longitude: %g, latitude: %g\n", b.lp.lam, b.lp.phi);
    }

    /* Clean up */
    proj_destroy (P);
    proj_context_destroy (C); /* may be omitted in the single threaded case */

}