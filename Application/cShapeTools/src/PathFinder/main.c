#include <stdio.h>
#include <stdlib.h>
#include <proj.h>
#include "../../include/PathFinder/process.h"

#define BOOL char
#define FALSE 0
#define TRUE 1

int main(void) {
    PJ_CONTEXT *C;
    PJ *P;
    PJ* P_for_GIS;
    PJ_COORD a, b, base;
    int i = 0;

    FILE *fptr;
    char filename[40];
    char ch;

    int line_nums = 0;
    printf("Enter file name: ");
    scanf("%s", filename);
    fptr = fopen(filename, "r");
    ch = getc(fptr);
    while (ch != EOF)
    {
        if (ch == '\n')
        {
            line_nums = line_nums + 1;
        }
        ch = getc(fptr);
    }
    rewind(fptr);
    printf("Number of lines: %d\n", line_nums);

    // static double longlat_array[1500000][2] = {0};
    double (*longlat_array)[line_nums] = malloc (sizeof(double[line_nums][2]));

    printf("Made it here\n");
    makeArray(longlat_array, line_nums, fptr);
    fclose(fptr);
    
    geoConversion(longlat_array, line_nums);
    base = proj_coord (45, -93, 0, 0);
    double (*distance) = malloc (sizeof(double)*line_nums);
    distanceCalc(longlat_array, distance, line_nums, base);
    free(longlat_array);
    free(distance);
    return 0;
}
