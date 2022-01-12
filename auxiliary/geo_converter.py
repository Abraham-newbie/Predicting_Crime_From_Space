import numpy as np
import pandas as pd
import geopandas
import fiona
from geopandas import GeoDataFrame



# Converting pandas.DataFrame to GeoDataFrame object and
# Converting pandas.Series to GeoSeries object
# Converting 'geomettry' column from being Series to GeoSeries so that the info inside is considered to be geospatial

def df_to_geo_df(df):
    df = GeoDataFrame(df)
    # Converting Series Object to GeoSeries
    df['geometry'] = geopandas.GeoSeries.from_wkt(df['geometry'])
    geo_df = geopandas.GeoDataFrame(df, geometry='geometry')
    
    return geo_df