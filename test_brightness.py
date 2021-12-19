import unittest

# All the neccessary Python packages
import numpy as np
import pandas as pd
import geopandas
import fiona
import geemap, ee
try:
        ee.Initialize()
except Exception as e:
        ee.Authenticate()
        ee.Initialize()

from brightness import brightness


class TestBrightnessIndexValue(unittest.TestCase):
    def test_brightness_index_for_buffer_zone(self):
        """
        Test that even one row of lat/lon point produces the expected answer
        """
        mean_ganja_expected = 0.6954635802568335
        b_df = pd.DataFrame(data = [["Ganja", 40.6879, 46.3723]], columns = ["AOI_Names", "Latitude", "Longitude"])
        result = brightness(date_from = "2020-10-01", date_to = "2020-10-31",
                            buffer_df = b_df, buffer_dist = 200000, band = "avg_rad", aoi_type = "buffer-zone", 
                            crs = "EPSG:4326", pathtomyshapefile = None, shp_column_name = None)
        mean_ganja_actual = result.iloc[0, 2]
        
        self.assertAlmostEqual(first = mean_ganja_expected, second = mean_ganja_actual, places=None, delta=0.08)
        
        
    def test_distinct_area_names(self):
        """
        Test that the names of the places are distinct
        """
        b_df = pd.DataFrame(data = [["Ganja", 40.6879, 46.3723], ["Ganja", 40.4093, 49.8671]], 
                            columns = ["AOI_Names", "Latitude", "Longitude"])
        
        
        
        with self.assertRaises(ValueError): brightness(date_from = "2020-10-01", date_to = "2021-01-31",
                                                   buffer_df = b_df, buffer_dist = 200000, band = "avg_rad", aoi_type = "buffer-zone", 
                                                   crs = "EPSG:4326", pathtomyshapefile = None, shp_column_name = None)
            
    
            
     

        
if __name__ == '__main__':
                         
    unittest.main()