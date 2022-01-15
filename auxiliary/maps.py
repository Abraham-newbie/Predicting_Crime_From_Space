import numpy as np
import pandas as pd
import geopandas
import os
import fiona
import matplotlib.pyplot as plt
import folium 
import auxiliary.geo_converter as gc
from geopandas import GeoDataFrame


def choropleth_by_pop(df_pop, df_shapefile, by = "interactive"):
    """ Returns the interactive or static plot of the population spread across neighborhoods in Portland
    Args:
        df_pop       (dataframe): The dataframe that includes population information
        df_shapefile (dataframe): The dataframe that includes the geospatial information
                                  regarding the corresponding neighborhoods
        by              (string): plots either static or interactive map. Default is interactive, if not default,
                                  then "static"
                                  As github is not rendered to display interactive maps created by
                                  folium package, but nbviewer is able to display it. Hence, both options
                                  are specified
    """
    # Merge Shapefile of Neighborhoods with crime dataset - Year 2015 is provided, but the population is same across years
    # as the controls used are only provided for the same one year, so here the purpose is not which year but rather
    # how dense is the population across the communities.
    population_2015 = df_pop[df_pop["Year"] == "2015"].groupby(["Matched_Names", "Year"])['adj_popn_pe_sq_mi'].mean().reset_index()

    shp_merged_with_crime_data = pd.merge(
                                            left=population_2015,
                                            right=df_shapefile,
                                            on='Matched_Names',
                                            how='left', 
                                             )
    shp_merged_with_crime_data = shp_merged_with_crime_data.drop_duplicates(subset = ['Matched_Names', 'Year'],
                                                                            keep = 'last').reset_index(drop = True)
    geo_df = gc.df_to_geo_df(df = shp_merged_with_crime_data)
    if by == "interactive":
        geo_df = geo_df.set_crs('epsg:3857')
        geo_map = folium.Map(location=[45.5152, -122.6784], zoom_start=11,tiles=None)
        folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(geo_map)

        #scale = (geo_df['adj_popn'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        scale = np.linspace(geo_df['adj_popn_pe_sq_mi'].min(), geo_df['adj_popn_pe_sq_mi'].max(), 6, dtype=int).tolist()
        scale[-1] = scale[-1] + 1

        geo_map.choropleth(
         geo_data=geo_df,
         name='Choropleth',
         data=geo_df,
         columns=['Matched_Names', 'adj_popn_pe_sq_mi'],
         key_on="feature.properties.Matched_Names",
         fill_color='BuPu',
         bins=scale,
         fill_opacity=1,
         line_opacity=0.2,
         legend_name='Population Density in Portland by Neighborhood (quantile scale)',
         smooth_factor=0
        )

        geo_map.save(os.path.join('./Figures', 'pop_density_interactive.html'))

        return geo_map
    elif by == "static":
        # Create the Choropleth Map of Population across Neighborhoods in Portland using Matplotlib
        fig, ax = plt.subplots(figsize=(11, 7))
        geo_df.plot(column='adj_popn_pe_sq_mi', cmap='Reds',  linewidth=1, ax=ax, edgecolor='0.9', legend=True)
        ax.axis('off')
        plt.title("Population Density of Neighborhoods in Portland")
        plt.savefig('Figures/pop_density_static.png', bbox_inches='tight')
        plt.show()
    else:
        raise NameError(f"{by} is not defined. Try using either of the 'interactive' or 'static' options for the plot")
        
        
        
        
        
def choropleth_by_crime(merged_df, shapefile, year = "2015", by = "interactive", type = "yearly"):
    """ Returns the interactive or static plot of the offernse rate spread across neighborhoods in Portland
    Args:
        merged_df       (dataframe): The dataframe that includes offenses information
        shapefile       (dataframe): The shapefile of Portland
        year            (string): The year from which one is interested to map the information
        by              (string): plots either static or interactive map. Default is interactive, if not default,
                                  then "static"
                                  As github is not rendered to display interactive maps created by
                                  folium package, but nbviewer is able to display it. Hence, both options
                                  are specified
        type            (string): Default is "yearly", which slices the dataframe such that only values from a certain year
                                  is processed for the map. The other option is "average", which feeds
                                  average value across years into the map. if year argument is provided, type = "yearly"
                                  Vice-versa, if type = "average", year = None
    """
    
    # Create a new column - Year
    merged_df["Year"] = merged_df.OccurMonth_Year.astype(str).str[:-3]
    # Group by the dataset by Neighborhood and Year, and calculate the crime rate for the years 2015 to 2021 by Neighborhood
    crime_rate_df = merged_df[["Matched_Names",
                              "Year", 
                              "adj_popn",
                              "Total_Offenses"]].groupby(["Matched_Names", "Year", 
                                                        "adj_popn"])["Total_Offenses"].sum().reset_index().eval('Offense_Rate_per_100k = (Total_Offenses / adj_popn) * 100000')
    if type == "yearly":
         
        shp_crime_rate = pd.merge(left=crime_rate_df,
                                  right=shapefile,
                                  on='Matched_Names',
                                  how='left', 
                                )
        shp_crime_rate = shp_crime_rate.drop_duplicates(subset = ['Matched_Names', 'Year'],
                                                        keep = 'last').reset_index(drop = True)
        # Crime Rate by Year
        shp_crime_rate = shp_crime_rate.loc[shp_crime_rate["Year"] == year, :]
        
    elif type == "average":

        ave_df = crime_rate_df[["Matched_Names",
                          "Year", 
                          "adj_popn",
                          "Offense_Rate_per_100k"]].groupby(["Matched_Names"])["Offense_Rate_per_100k"].mean().reset_index()
        shp_crime_rate = pd.merge(left=ave_df,
                                      right=shapefile,
                                      on='Matched_Names',
                                      how='left', 
                                    )
        shp_crime_rate = shp_crime_rate.drop_duplicates(subset = ['Matched_Names'],
                                                            keep = 'last').reset_index(drop = True)

       
    

    # Converting the dataframe to GeodDataframe
    geo_df = gc.df_to_geo_df(df = shp_crime_rate)
    if by == "interactive":
        if geo_df.crs is None:
            geo_df = geo_df.set_crs('epsg:3857')
        # Interactive Leaflet Choropleth Map centered at lat-lon of Portland using Folium
        geo_map = folium.Map(location=[45.5152, -122.6784], zoom_start=11,tiles=None)
        folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(geo_map)


        #scale = (geo_df['adj_popn'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        scale = np.linspace(geo_df['Offense_Rate_per_100k'].min(), geo_df['Offense_Rate_per_100k'].max(), 6, dtype=int).tolist()
        scale[-1] = scale[-1] + 1

        geo_map.choropleth(
         geo_data=geo_df,
         name='Choropleth',
         data=geo_df,
         columns=['Matched_Names', 'Offense_Rate_per_100k'],
         key_on="feature.properties.Matched_Names",
         fill_color='BuPu',
         bins=scale,
         fill_opacity=1,
         line_opacity=0.2,
         legend_name='Total Offenses Rate in Portland by Neighborhood (per 100,000)',
         smooth_factor=0
        )
        geo_map.save(os.path.join('./Figures', f'offense_Rate_per100k_portland_{year}.html'))
        
        return geo_map
        
        
    elif by == "static":
        # Create the static Choropleth Map of Population across Neighborhoods in Portland
        fig, ax = plt.subplots(1, figsize=(11, 7))
        geo_df.plot(column='Offense_Rate_per_100k', cmap='viridis_r',  linewidth=1, ax=ax, edgecolor='0.9', legend=True)
        ax.axis('off')
        if type == "yearly":
            plt.title(f"Crime Rate per 100000 by Neighborhoods in Portland for the year {year}")
            plt.savefig('Figures/CrimeRateper100k_static.png', bbox_inches='tight')
        elif type == "average":
            plt.title("Average Offense Rate per 100000 by Neighborhoods in Portland for the years 2015 - 2021")
            plt.savefig('Figures/AveCrimeRateper100k_static.png', bbox_inches='tight')
        
        plt.show()
    else:
        raise NameError(f"{by} is not defined. Try using either of the 'interactive' or 'static' options for the plot")
        
        
        
        
        
def choropleth_by_brightness(df, shapefile, year = "2015", by = "static"):
    merged_shp_brightness = shapefile.merge(df[df["Year"] == year], 
                          left_on = "Matched_Names",
                          right_on = "Names of Places", 
                          how = "left")
    
    # Converting the dataframe to GeodDataframe
    geo_df = gc.df_to_geo_df(df = merged_shp_brightness)
    if by == "interactive":
        if geo_df.crs is None:
            geo_df = geo_df.set_crs('epsg:3857')
        # Add text to the map to list top 5 and last 5 neighborhoods for the 
        # Annual Average of Average Radiance per pixel per month
        df_br = merged_shp_brightness[['Matched_Names', 'Average Radiance Per Pixel Per month']].copy(deep=True)
        df_br.sort_values('Average Radiance Per Pixel Per month', ascending=False, inplace=True)
        df_br.reset_index(drop=True, inplace=True)
        df_br.index += 1

        legend_top = '\n'.join(df_br.head().to_string().split('\n')[1:])
        legend_last = '\n'.join(df_br.tail().to_string().split('\n')[1:])
        legend_html =   '''
                        <div style="position: fixed; 
                                    top: 100px; right: 50px; width: 300px; height: 300px; 
                                    border:2px solid blue; z-index:9999; font-size:14px;">
                                    &nbsp; <br>
                                    &nbsp; <br>
                                    Ranking: Annual average of Brightness by Neighborhoods in Portland
                                    {} 
                                    ......  
                                    {}
                        </div>
                        '''
        legend_html = legend_html.format(legend_top,legend_last)
        legend_html = legend_html.replace('\n','<br> ')

        # Interactive Leaflet Choropleth Map centered at lat-lon of Portland using Folium
        geo_map = folium.Map(location=[45.5152, -122.6784], zoom_start=11,tiles=None)
        folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(geo_map)
        geo_map.get_root().html.add_child(folium.Element(legend_html))
        scale = np.linspace(geo_df['Average Radiance Per Pixel Per month'].min(), 
                            geo_df['Average Radiance Per Pixel Per month'].max(), 6, dtype=int).tolist()
        scale[-1] = scale[-1] + 1

        geo_map.choropleth(
         geo_data=geo_df,
         name='Choropleth',
         data=geo_df,
         columns=['Matched_Names', 'Average Radiance Per Pixel Per month'],
         key_on="feature.properties.Matched_Names",
         fill_color='BuPu',
         bins=scale,
         fill_opacity=1,
         line_opacity=0.2,
         legend_name=f'Annual Average of average Radiance in {year}',
         smooth_factor=0
        )
        geo_map.save(os.path.join('./Figures', f'Brightness_interactive{year}.html'))
        return geo_map
    
    elif by == "static":
        # Create the Choropleth Map of Population across Neighborhoods in Portland
        fig, ax = plt.subplots(1, figsize=(11, 7))
        geo_df.plot(column='Average Radiance Per Pixel Per month', cmap='viridis_r', 
                    linewidth=1, ax=ax, edgecolor='0.9', legend=True)


        ax.axis('off')
        plt.title(f"Annual Average of the brightness by Neighborhoods in Portland for the year {year}")
        plt.savefig(f'Figures/Brightness_static{year}.png', bbox_inches='tight')

        plt.show()