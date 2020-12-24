!# /bin/bash

ls -d ../../webapp/modules/geotools/geotools/data/new_parcels/* | grep .shp$ | xargs ../cShapeTools/bin/ShapeFileFixer