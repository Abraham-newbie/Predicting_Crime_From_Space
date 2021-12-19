# This file will drop All-NaN columns in the crime dataset, concat over the years, match the neighborhood names with those in shapefiles.


# Install the necessary packages
import pandas as pd
import numpy as np
import difflib 





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
    
    return df_new





def matching_names(df1, df2, c1, c2):
    """Match the names in one file with another and create a new column and join it as a new column to the existing dataframe
    
    Args:
        df1 (dataframe): a dataframe whose column value names to be matched
        df2 (dataframe): a dataframe to match the names with
        c1  (column): a column to be matched in df1
        c2  (column): a column to match with in df2
    
    Returns:
        df1 (dataframe): a dataframe extended with the matched column as a new column
    """

    l1 = sorted(list(df1[c1].dropna().unique()))
    l = []
    for i in l1:
        newstring = i.upper()
        l.append(newstring)

    list_strings = []
    for string in l:
        matched = difflib.get_close_matches(string, df2[c2], cutoff = 0.5)[:1] or [None]
        list_strings.append(matched)
    unlisted_list = [item for sublist in list_strings for item in sublist]
    dictionary = {"matched_names": unlisted_list, 
              "old_NAME": sorted(list(df1[c1].dropna().unique()))}
    matched_names_df = pd.DataFrame(data = dictionary)
    
    # Match manually those that are not correctly matched with difflib.get_close_matches function
    matched_names_df.loc[matched_names_df["old_NAME"]== "Wilkes", "matched_names"] = "WILKES COMMUNITY GROUP"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Sunderland", "matched_names"] = "SUNDERLAND ASSOCIATION OF NEIGHBORS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Southwest Hills", 
                         "matched_names"] = "SOUTHWEST HILLS RESIDENTIAL LEAGUE"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Sabin", "matched_names"] = "SABIN COMMUNITY ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Centennial", "matched_names"] = "CENTENNIAL COMMUNITY ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Cully", "matched_names"] = "CULLY ASSOCIATION OF NEIGHBORS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Healy Heights", 
                         "matched_names"] = "HEALY HEIGHTS/SOUTHWEST HILLS RESIDENTIAL LEAGUE"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Lloyd", "matched_names"] = "LLOYD DISTRICT COMMUNITY ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Irvington", "matched_names"] = "IRVINGTON COMMUNITY ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Northwest", "matched_names"] = "NORTHWEST DISTRICT ASSOCIATION"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Northwest Heights", "matched_names"] = "NORTHWEST HEIGHTS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Parkrose", 
                         "matched_names"] = "PARKROSE"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Parkrose Heights", "matched_names"] = "PARKROSE HEIGHTS ASSOCIATION OF NEIGHBORS"
    matched_names_df.loc[matched_names_df["old_NAME"]== "Buckman West", "matched_names"] = "BUCKMAN COMMUNITY ASSOCIATION"
    
    # Drop the unmatched row values
    df1 = df1[~df1[c1].isin(["Northwest Industrial"])]
    
    # Create a new column with matched names
    matched_names_df = matched_names_df[~matched_names_df["old_NAME"].isin(["Northwest Industrial"])]
    matched_names_dict = dict(zip(matched_names_df["old_NAME"], matched_names_df["matched_names"]))
    df1["Matched_Names"] = df1[c1].map(matched_names_dict)
    
    
    
    return df1


