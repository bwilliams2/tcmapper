#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include "./process.h"


void makeArray(double longlat[][2], int numrows, FILE *ifp) {
    int i=0, j=0, numcols = 2, ch;
    double lon, lat;

    for (i=0; i < numrows; ++i) {
        fscanf(ifp, "%lf %lf", &lon, &lat);
        longlat[i][0] = lon;
        longlat[i][1] = lat;
        // for (j=0; j < 2; ++j) {
        //     while (((ch = getc(ifp)) != EOF) && (ch == ' ')) // eat all spaces
        //     if (ch == EOF) break;                            // end of file -> break
        //     ungetc(ch, ifp);
        //     if (fscanf("%lf", &num) != 1) break;
        //     longlat[i][j] = num;                              // store the number
        // }
    }
}


void distanceCalc(double longlat_array[][2], double * distance, int line_nums, PJ_COORD base) {
    int i;
    PJ_CONTEXT *C;
    PJ *P;
    PJ* P_for_GIS;
    PJ_COORD a, b;

    // Store distance calculations
    C = proj_context_create();

    P = proj_create_crs_to_crs (C,
                                "EPSG:4326",
                                "EPSG:4326",
                                NULL);
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

    for (i = 0; i < line_nums; ++i) {
        a = proj_coord (longlat_array[i][0], longlat_array[i][1], 0, 0);
        distance[i] = proj_lp_dist (P, a, base);
    }

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