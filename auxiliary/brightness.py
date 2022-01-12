# All the neccessary Python packages
### Import numpy and pandas, geopandas, and os
import numpy as np
import pandas as pd
import geopandas
import fiona
import os
### Import geemap, and ee:
import geemap, ee
### Initialize ee
try:
        ee.Initialize()
except Exception as e:
        ee.Authenticate()
        ee.Initialize()

        
        
        
def brightness(date_from, date_to, buffer_df, buffer_dist, band = "avg_rad", aoi_type = "buffer-zone", 
               crs = "EPSG:4326", pathtomyshapefile = None, shp_column_name = None):
    """ Derives Average Monthly Radiance Index for the given AOI and for the given date/period
    
    Args:
        date_from        (ISO date format): YYYY-MM-DD (e.g. 2015-01-01)
        date_to          (ISO date format): YYYY-MM-DD (e.g. 2015-01-31) 
                                * Since VIIRS image collection comprises monthly composites,
                                to derive brightness index for a month, e.g. December 2016, one needs to write it as:
                                date_from = 2016-12-01, date_to = 2016-12-31
                                This will give us one value for Brightness index for a given point on Earth.
                                * To derive the Average Monthly Radiance Index for a given AOI across multiple years, e.g., 
                                from 2014 January till 2021 Mai, the following should be set as the appropriate date:
                                date_from = 2014-01-01, date_to = 2021-05-31
        buffer_df          (dataframe):  * If aoi_type = "shapefile", then buffer_df = None, as we will be supplying
                                        pathtomyshapefile. 
                                        * If aoi_type = "buffer-zone", then buffer_df takes in a dataframe, with three columns:
                                        - "Latitude"
                                        - "Longitute"
                                        - "AOI_Names"
                                        Note:
                                        Names of AOI (in "AOI_Names") should be DISTINCT.
                                        Latitude and Longitude points should be in decimal degrees.
                                        There should be no missing values (If there is, they should be dropped
                                        before feeding it into this function)
        buffer_dist         (integer):  The distance value by which we want to take the buffer zone around the lat/lon point
                                        Ex: 50 km buffer zone around a point should be written as buffer_df = 50000.
                                        If shapefile is used, buffer_dist = None
                     
        band             (str.):      Default is "avg_rad", which stands for Average DNB radiance values
                                and the other option to use is "cf_cvg", which means Cloud-free coverages, This band 
                                can be used to identify areas with low numbers of observations where the quality is reduced.
        aoi_type          (str.):     Default is "buffer_zone", and the other option is "shapefile". 
                                * "buffer-zone" means that the dataset that is supplied in buffer_df is a dataframe
                                with latitude, longitude points corresponding to different AOI on Earth. 
                                Visually, this dataframe has three columns, one corresponding to names of Areas of Interest,
                                the other two being Latitude and Longitude points. Names of AOI should be DISTINCT.
                                Latitude and Longitude points should be in decimal degrees. 
                                * "shapefile" means that the dataset that is supplied in pathtomyshapefile 
                                is a shapefile of all the Areas of Interest.
        crs                (str.):     Default is "EPSG:4326", which is also the only accepted CRS format by geemap. 
                                 If the supplied crs is different from "EPSG:4326", then it will be converted to "EPSG:4326".
        pathtomyshapefile  (a directory path): Default is None. To import the shapefile with geemap, a path to your shapefile 
                                 should be given. The directory where your .shp (shapefile) is located should also include 
                                 .dbf, .cpg, .prj, .shx extension files that comes with a usual shapefile folder. 
        shp_column_name    (str.):     Name of the column in the dataframe inside **pathtomyshapefile
                                  where Areas of Interest; e.g., cities, markets, neighborhoods, 
                                  places, countries etc., are located. 
                                  * Except spaces/dot/comma/slashes there should be no other character 
                                  supplied inbetween the names of places in this column
                                  Example: The name of a place written as Northwest@Aaron should be avoided.
                                  The name of a place written as 'Northwest Industrial' 
                                  or 'Northwest Industrial/Northwest Neighborhood' is allowed
                                  Note: if aoi_type = "buffer-zone", then shp_column_name = None
                   
        
                                
      Returns:
          brightness_index           (dataframe): Average Monthly Radiance Index
          shapefile_dataframe_format (.csv file): Convert the CRS of a shapefile to "EPSG:4326", if it is not 
                                                  in that Reference system, and saves the shapefile for a future reference 
                                                  as a csv file in the directory where this jupyter notebook is located.
          ./AOI_DataSets/Shapefiles  (directory): is a directory that is generated using brightness() function, where 
                                                  each area/place in the one common shapefile inside pathtomyshapefile
                                                  is exported to this directory as seperate shapefiles. 
                                                  
          
  
    """
    
    
    # Selecting the Image collection for the all years, for which VIIRS dataset is available: 2014-01-01 - 2021-05-01
    # NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG is simply the complete dataset
    # For the Dataset - VIIRS Stray-light Corrected Day/Night Band composites -  there are two bands available: 
    # avg_rad(=Average DNB radiance values.) 
    # cf_cvg (=Cloud-free coverages, This band can be used to identify areas with low numbers of observations 
    # where the quality is reduced.) 

    viirs = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG").filterDate(date_from, date_to).select(band)
    
    if aoi_type == "buffer-zone":
        if len(buffer_df["AOI_Names"].unique()) != len(buffer_df):
            raise ValueError("The names of the places in AOI_Names column are not distinct. "
                            "The number of distinct place names and the length of the dataframe does not match.")
 
    
    if aoi_type == "shapefile":
        
        aoi_shp = pathtomyshapefile
        data = geopandas.read_file(aoi_shp)
        data.to_csv("shapefile_dataframe_format.csv")
        
        
        if crs != "EPSG:4326":
            # Change the CRS of our shapefile to EPSG:4326
            data = data.to_crs(epsg=4326)
            
        # Import the shapefile with geemap
        aois = geemap.shp_to_ee(aoi_shp)
        
        ### Export each area/place into seperate shapefiles
        
         # 1. Group the data by column where AOI is filled in (inside the shapefile dataframe, in pathtomyshapefile)
        grouped = data.groupby(shp_column_name)
        # 2. Import os -module that is useful for parsing filepaths
        # 3. Determine output directory
        output_directory = "AOI_DataSets"
        # 4. Create a new folder called 'Shapefiles'
        sub_folder = os.path.join(output_directory, 'Shapefiles')
        # 5. Check if the folder exists already
        if not os.path.exists(sub_folder):
            # 6. If it does not exist, create one
            os.makedirs(sub_folder)
        # 7. Iterate over the groups
        for key, values in grouped:
            # 8. Format the filename (replace spaces/comma/slashes with underscores,
            # dot with "" using 'replace()' -function)
            output_name = "%s.shp" % key.replace(" ", "_").replace("/", "_").replace(".", "").replace(",", "_")

            # Print some information for the user
            # print("Processing: %s" % key)

            # 9. Create an output path
            outpath = os.path.join(sub_folder, output_name)

            # 10. Export the data
            values.to_file(outpath)
        
        # Collecting all the shapefiles in a list
        DIR = "./AOI_DataSets/Shapefiles"
        areas_list = []
        for subdir in os.listdir(DIR):
            if subdir.endswith(r"shp"):
                areas_list.append(os.path.join(DIR, subdir))
    
    # First we need to create a list of feautures in the form of 
    #[ee.Feature(ee.Geometry.Point(latitude, longitude).buffer(km)),..] or
    #[ee.Feature(imported_shapefile.geometry(), ..]
    #for all the areas of interest. 
    # Specifically, a Feature is an object with a geometry property storing a Geometry object (or null)
    # and a properties property storing a dictionary of other properties.
    
        features = []
        for i in areas_list:
            area = geemap.shp_to_ee(i)
            features.append(ee.Feature(area.geometry(),
                                      {'name': i.split("Shapefiles\\", 1)[1][:-4]}))
        # Areas Names
        areas_names = []
        for i in areas_list:
            name = i.split("Shapefiles\\", 1)[1][:-4]
            areas_names.append(name)
    elif aoi_type == "buffer-zone":
        
        features = []
        for i in range(0, len(buffer_df)):
            features.append(ee.Feature(ee.Geometry.Point([buffer_df.loc[i,"Longitude"],
                                                          buffer_df.loc[i, "Latitude"]]).buffer(buffer_dist),
                                                          {'name': buffer_df["AOI_Names"][i]}))

        
        
    # Given the list of features, we are going to create a Feature Collection for our areas of interest
    aoi_fc = ee.FeatureCollection(features)
    # function to reduce our collection of geometries
    def get_city_avg_rad(img):
        return img.reduceRegions(reducer=ee.Reducer.mean(), collection=aoi_fc, scale=500)

    # function to get individual img dates
    def get_date(img):
        return img.set('date', img.date().format())

    # map these functions to our image collection
    reduced_cities = viirs.map(get_city_avg_rad).flatten()
    dates = viirs.map(get_date)

    # get lists
    key_cols = ['name','mean']
    cities_list = reduced_cities.reduceColumns(ee.Reducer.toList(len(key_cols)), key_cols).values()
    dates_list = dates.reduceColumns(ee.Reducer.toList(1), ['date']).values()

    # some numpy maneuvers to structure our data
    if np.asarray(cities_list.getInfo()).squeeze().shape == (2,):
        df = pd.DataFrame(np.asarray(cities_list.getInfo()).squeeze()).T
        df.columns = key_cols
    else:
        df = pd.DataFrame(np.asarray(cities_list.getInfo()).squeeze(), columns = key_cols)
    dates = np.asarray(dates_list.getInfo()).squeeze()

    
    if aoi_type == "shapefile":
        for c in areas_names:
            df.loc[df['name']==c,'dates'] = dates
    elif aoi_type == "buffer-zone":
        for c in buffer_df["AOI_Names"]:
            df.loc[df['name']==c,'dates'] = dates

    # as we've done before, convert date and set index
    df['dates'] = pd.to_datetime(df['dates'])
    df.set_index('dates', inplace=True)

    # we'll also convert our mean datatype to float
    df['mean'] = df['mean'].astype(float)
    df.columns = ["Names of Places", "Average Radiance Per Pixel Per month"]
    df.reset_index(inplace = True)
 
    
    return df
    




    
    
    
# Identifying the crs of the shapefile
def identify_crs(pathtomyshapefile):
    file = fiona.open(pathtomyshapefile)
    crs = file.crs
    v = [value for key, value in crs.items()]
    return v[0]
