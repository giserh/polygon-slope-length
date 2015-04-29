#!/usr/bin/env python

"""Calculating slope length rasters for polygons from a DEM using
ArcPy and SAGA GIS"""

import arcpy
import subprocess
import os
import sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

arcpy.env.overwriteOutput = True


def runCommand_logged(cmd, logstd, logerr):
    p = subprocess.call(cmd, stdout=logstd, stderr=logerr)

# Define error logging variables.

WORKDIR = r"D:\data\working_dir"
STDLOG = WORKDIR + os.sep + "import.log"
ERRLOG = WORKDIR + os.sep + "import.error.log"

logstd = open(STDLOG, "a")
logerr = open(ERRLOG, "a")

# Create search cursor for polygon shapefile.

fc = r"D:\data\working_dir\polygons.shp"
cursor = arcpy.SearchCursor(fc)

# Global Variables.

dem = r"D:\data\working_dir\dem.tif"
clipping_poly = r"D:\data\working_dir\clip_poly.shp"
clipped_dem_path = "D:\data\working_dir\clipped_rasters\\"
slope_output_path = "D:\data\working_dir\slope_out\\"


def poly_clip_dem(clip_poly, clip_raster_path):

    # Selects individual polygons and clips DEM.

    extension = row.POLY_ID[3:]     # For saving files (<13 chars for grids)
    out_raster = clip_raster_path + extension + ".tif"

    arcpy.Select_analysis(fc, clip_poly, '"POLY_ID" = '+"'"+row.POLY_ID+"'")
    arcpy.Clip_management(dem, "#", out_raster, clip_poly, "-999", "ClippingGeometry")


def saga_raster_conversion(clip_raster_path):

    # SAGA raster conversion (.tif to .sgrd)

    extension = row.POLY_ID[3:]    # For saving files (<13 chars for grids)
    out_raster = clip_raster_path + extension + ".tif"
    out_raster_path = out_raster[:-4]   # Remove .tif

    cmd = 'saga_cmd io_gdal 0 -GRIDS ' + out_raster_path + '.sgrd' + ' -FILES ' + out_raster + ' -TRANSFORM TRUE -INTERPOL 1'

    try:
        runCommand_logged(cmd, logstd, logerr)
    except Exception, e:
        logerr.write("Exception thrown")
        logerr.write("ERROR: %s\n" % e)


def saga_slope_length(clip_raster_path, slope_path):

    # Runs SAGA Slope Length module.

    extension = row.POLY_ID[3:]
    slope_input = clip_raster_path + extension + '.sgrd'
    slope_output = slope_path + 'slpl_' + extension + '.sgrd'

    cmd = 'saga_cmd ta_hydrology 7 -DEM ' + slope_input + ' -LENGTH ' + slope_output

    try:
        runCommand_logged(cmd, logstd, logerr)
    except Exception, e:
        logerr.write("Exception thrown")
        logerr.write("ERROR: %s\n" % e)

# Count number of all features.

count_all_features = 0

for row in cursor:
    count_all_features += 1

del row, cursor


# Iterate through polygons and generate slope length rasters.

cursor = arcpy.SearchCursor(fc)
count_row = 0

for row in cursor:

    poly_clip_dem(clipping_poly, clipped_dem_path)
    saga_raster_conversion(clipped_dem_path)
    saga_slope_length(clipped_dem_path, slope_output_path)

    count_row += 1
    print str(count_row) + " of " + str(count_all_features) + " processed."

del row, cursor

print "Complete!"
