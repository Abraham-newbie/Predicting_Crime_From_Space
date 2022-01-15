# This file will drop All-NaN columns in the crime dataset, concat over the years, match the neighborhood names with those in shapefiles.


# Install the necessary packages
import pandas as pd
import numpy as np
import difflib 
# Catch and ignore the warnings
import warnings
warnings.filterwarnings("ignore")





def drop_nan_and_uncommon_and_concat(dataframes):
    """Concats the datasets into one,
       drops uncommon columns and those with all-NaN values
    
    Args:
        dataframes (list): a list of dataframes in pandas
    
    Returns:
        dataframe (dataframe): a concatted dataset with dropped columns of all-NaN values and dropped uncommon columns
    """
    # Drop all the columns with all "NaN"s
    dropped_nans = []
    for df in dataframes:
        df = df.dropna(axis=1, how='all')
        dropped_nans.append(df)
    # Keep only common columns while concatting the dataframes
    df_new = pd.concat(dropped_nans,join='inner', ignore_index=True)
    
    
    df_new["OccurDate"] = pd.to_datetime(df_new["OccurDate"],format='%d/%m/%Y', infer_datetime_format=True)
    
    
    df_new['OccurMonth_Year']  = pd.to_datetime(df_new['OccurDate']).dt.to_period('M')
    to_drop = ['Address',
               'CrimeAgainst',
               'OffenseType',
               'OpenDataLat',
               'OpenDataLon',
               'ReportDate']

    


    df_new = df_new[df_new.OccurMonth_Year>"2015-06-01"]
    df_new = df_new[df_new.OccurMonth_Year<"2021-06-01"]

    df_new.drop(to_drop, inplace=True, axis=1)
    df_new["Neighborhood"] = df_new.Neighborhood.str.upper()
    
    return df_new





def matching_names(df1, df2, c1, c2):
    """Match the names in one file with another and create a new column and join it as a new column to the existing dataframe
    
    Args:
        df1 (dataframe): a dataframe whose column value names to be matched (crime_data)
        df2 (dataframe): a dataframe to match the names with  (brightness_index)
        c1  (column): a column to be matched in df1  ("Neighborhood")
        c2  (column): a column to match with in df2  ("Names of Places")
    
    Returns:
        df1 (dataframe): a dataframe extended with the matched column as a new column
    """

    l1 = sorted(list(df1[c1].dropna().unique()))
    l = []
    for i in l1:
        newstring = i.upper()
        l.append(newstring)
        
    list_unintersected = ["SABIN_COMMUNITY_ASSN_IRVINGTON_COMMUNITY_ASSN", "SULLIVAN'S_GULCH_GRANT_PARK",
                          "SYLVAN-HIGHLANDS_SOUTHWEST_HILLS_RESIDENTIAL_LEAGUE", 
                          "PLEASANT_VALLEY_POWELLHURST-GILBERT", "ROSEWAY_MADISON_SOUTH", "HILLSIDE_NORTHWEST_DISTRICT_ASSN", 
                          "LENTS_POWELLHURST-GILBERT", "LLOYD_DISTRICT_COMMUNITY_ASSN_SULLIVAN'S_GULCH", 
                          "MC_UNCLAIMED_#11",  "MC_UNCLAIMED_#13", "MC_UNCLAIMED_#14", "MC_UNCLAIMED_#5", 
                          "EASTMORELAND_REED", "EASTMORELAND_ARDENWALD-JOHNSON_CREEK", "FOREST_PARK_LINNTON",
                          "FOREST_PARK_NORTHWEST_DISTRICT_ASSOCIATION", 
                          "GOOSE_HOLLOW_FOOTHILLS_LEAGUE_SOUTHWEST_HILLS_RESIDENTIAL_LEAGUE", 
                          "GRANT_PARK_HOLLYWOOD", "HAZELWOOD_MILL_PARK", "ALAMEDA_BEAUMONT-WILSHIRE", 
                          "ALAMEDA_IRVINGTON_COMMUNITY_ASSN", "ASHCREEK_CRESTWOOD", "ARDENWALD-JOHNSON_CREEK_WOODSTOCK", 
                          "ARGAY_WILKES_COMMUNITY_GROUP", "BOISE_ELIOT", "ARLINGTON_HEIGHTS_SYLVAN-HIGHLANDS",
                          "BRIDLEMILE_SOUTHWEST_HILLS_RESIDENTIAL_LEAGUE", "CENTENNIAL_COMMUNITY_ASSN_PLEASANT_VALLEY"]
    
    df2 = df2.loc[~df2[c2].isin(list_unintersected)]

    list_strings = []
    for string in l:
        matched = difflib.get_close_matches(string, df2[c2].unique(), cutoff = 0.5)[:1] or [None]
        list_strings.append(matched)
    unlisted_list = [item for sublist in list_strings for item in sublist]
    dictionary = {"matched_names": unlisted_list, 
              "old_NAME": sorted(list(df1[c1].dropna().unique()))}
    matched_names_df = pd.DataFrame(data = dictionary)
    matched_names_df.loc[matched_names_df["old_NAME"]== "WILKES", "matched_names"] = "WILKES_COMMUNITY_GROUP"
    matched_names_df.loc[matched_names_df["old_NAME"]== "SUNDERLAND", "matched_names"] = "SUNDERLAND_ASSOCIATION_OF_NEIGHBORS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "SOUTHWEST HILLS", 
                         "matched_names"] = "SOUTHWEST_HILLS_RESIDENTIAL_LEAGUE"
    matched_names_df.loc[matched_names_df["old_NAME"]== "SABIN", "matched_names"] = "SABIN_COMMUNITY_ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "CENTENNIAL", "matched_names"] = "CENTENNIAL_COMMUNITY_ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "CULLY", "matched_names"] = "CULLY_ASSOCIATION_OF_NEIGHBORS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "HEALY HEIGHTS", 
                         "matched_names"] = "HEALY_HEIGHTS_SOUTHWEST_HILLS_RESIDENTIAL_LEAGUE"
    matched_names_df.loc[matched_names_df["old_NAME"]== "LLOYD", "matched_names"] = "LLOYD_DISTRICT_COMMUNITY_ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "IRVINGTON", "matched_names"] = "IRVINGTON_COMMUNITY_ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "NORTHWEST", "matched_names"] = "NORTHWEST_DISTRICT_ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "NORTHWEST HEIGHTS", "matched_names"] = "NORTHWEST_HEIGHTS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "PARKROSE", 
                         "matched_names"] = "PARKROSE"
    matched_names_df.loc[matched_names_df["old_NAME"]== "PARKROSE HEIGHTS",
                         "matched_names"] = "PARKROSE_HEIGHTS_ASSOCIATION_OF_NEIGHBORS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "BUCKMAN EAST", "matched_names"] = "BUCKMAN_COMMUNITY_ASSOCIATION"
    #matched_names_df.loc[matched_names_df["old_NAME"]== "BUCKMAN WEST", "matched_names"] = "BUCKMAN_COMMUNITY_ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "SUMNER", "matched_names"] = "SUMNER_ASSOCIATION_OF_NEIGHBORS"
    
    
    # Drop the unmatched row values
    df1 = df1[~df1[c1].isin(["NORTHWEST INDUSTRIAL", "BUCKMAN WEST"])]
    
    # Create a new column with matched names
    matched_names_df = matched_names_df[~matched_names_df["old_NAME"].isin(["NORTHWEST INDUSTRIAL", "BUCKMAN WEST"])]
    matched_names_dict = dict(zip(matched_names_df["old_NAME"], matched_names_df["matched_names"]))
    df1["Matched_Names"] = df1[c1].map(matched_names_dict)
    warnings.warn("A value is trying to be set on a copy of a slice from a DataFrame.")
    
    
    
    return df1





def merge(df_index, df_matched, type = "night"):
    """Merges the brightness index with crime data
    
    Args:
        df_index   (dataframe): brightness_index
        df_matched (dataframe): Crime dataset, whose Neighborhood Column values are matched with those in brightness_index (crime data)
        type          (string): Takes in "night", "day", or "all"; whether one wants to keep the entries for 
                                offenses thaat happened furing night, during daytime or both. Default is "night". 
    
    Returns:
        df_merged (dataframe): crime dataset that is merged with brightness_index
    """

    
    
    #df_index.rename(columns = {"Names of Places": "Matched_Names"}, inplace = True)
    df_index['OccurMonth_Year']  = pd.to_datetime(df_index['dates']).dt.to_period('M')
    df_index['OccurMonth_Year'] = df_index['OccurMonth_Year'].astype('str')
    df_matched['day_or_night'] = np.where(((df_matched['OccurTime']<700) | (df_matched['OccurTime']>2000)), 'night', 'day')
    warnings.warn("A value is trying to be set on a copy of a slice from a DataFrame.")
    if type == "night":
        df_matched=df_matched[df_matched['day_or_night']=='night'] 
        data_to_convert=df_matched
    elif type == "day":
        df_matched=df_matched[df_matched['day_or_night']=='day']
        data_to_convert=df_matched
    else:
        data_to_convert=df_matched
        

    #data_to_convert=df_matched
    df_wide= data_to_convert.groupby(['OccurMonth_Year','Neighborhood',
                                      'OffenseCategory', "Matched_Names"]).OffenseCount.sum().reset_index()
    df_wide= df_wide.pivot_table(index=["Neighborhood","OccurMonth_Year", "Matched_Names"], 
                                columns='OffenseCategory',
                                 values='OffenseCount').reset_index()
    df_wide = df_wide.replace(np.nan, 0)
    df_wide['Total_Offenses']= df_wide.iloc[:,4:].sum(axis=1)
    df_wide=df_wide.reset_index()
    match_df = pd.merge(
    left=df_wide,
    right=df_index,
    left_on = ['Matched_Names','OccurMonth_Year'], 
    right_on = ['Names of Places', 'OccurMonth_Year'],
    how='left'
     )
    
    return match_df



def add_controls(df_merged):
    """Adds Controls to the crime data
    
    Args:
        df_merged (dataframe): crime dataset that is merged with brightness_index
    
    Returns:
        df_with_controls (dataframe): crime dataset with controls
    """
    
    
    xl = pd.ExcelFile('data/neighborhood_controls.xlsx', engine = 'openpyxl')
    controls = xl.parse('Sheet1')
    controls=controls.replace({'Neighborhood': {'ARDENWALD-JOHNSON CREEK': 'ARDENWALD',
                                            'BRENTWOOD/ DARLINGTON': 'BRENTWOOD-DARLINGTON',
                                            'NORTHWEST DISTRICT': 'NORTHWEST',
                                            'ST. JOHNS': 'ST JOHNS',
                                            'LLOYD DISTRICT': 'LLOYD',
                                            "SULLIVAN’S GULCH": "SULLIVAN'S GULCH" ,
                                            'LLOYD DISTRICT': 'LLOYD',
                                            'OLD TOWN/ CHINATOWN': 'OLD TOWN/CHINATOWN',  
                                            'BUCKMAN' : 'BUCKMAN EAST',
                                           }})
    df_with_controls = pd.merge(
                                        left=df_merged,
                                        right=controls,
                                        on='Neighborhood',
                                        how='left'
                                         )
    
    return df_with_controls




