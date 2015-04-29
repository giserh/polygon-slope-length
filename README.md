# polygon-slope-length


This python script calculates slope length rasters within polygons from a dem using **ArcPy** and **SAGA GIS**.

![slpl]

[slpl]: https://raw.githubusercontent.com/simonkiley/polygon-slope-length/master/slope_length.png
        



## Usage

There are several variables within the script that need to be set before running, mainly:

```python
fc = "D:\data\working_dir\polygons.shp"  # Polygon feature class
dem = "D:\data\working_dir\dem.tif"
clipping_poly = "D:\data\working_dir\clip_poly.shp" # Temporary output, will be overwritten. 
clipped_dem_path = "D:\data\working_dir\clipped_rasters\\"
slope_output_path = "D:\data\working_dir\slope_out\\"
```

[SAGA GIS](http://sourceforge.net/projects/saga-gis/) and ArcGIS 10.x must be installed with an available Spatial Analyst license. 
