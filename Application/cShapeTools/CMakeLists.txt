cmake_minimum_required(VERSION 3.16)

# Definitions
set(PROJECT_NAME GeoDesicPath)
project(${PROJECT_NAME})

add_subdirectory(src/PathFinder)
add_subdirectory(src/ShapeFileFixer)