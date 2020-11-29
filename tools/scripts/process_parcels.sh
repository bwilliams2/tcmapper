!# /bin/bash

ls -d ../../webapp/modules/geotools/geotools/data/new_parcels/* | grep Points.shp$ | xargs ../cShapeTools/bin/ShapeFileFixer