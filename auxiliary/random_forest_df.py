import datetime as dt
import numpy as np
import pandas as pd
    
    
def relevant_offenses_df(df, list_col):
    # Read the data
    df_rf = df[list_col] 
    # Drop the rows with missing values
    df_rf.dropna(inplace = True)
    # Year and Month column being set as datetime
    df_rf['OccurMonth_Year'] = pd.to_datetime(df_rf['OccurMonth_Year'], errors='coerce')
    df_rf["Year"] = df_rf['OccurMonth_Year'].dt.year
    df_rf["Month"] = df_rf['OccurMonth_Year'].dt.month
    # neighborhoods having entries for each month from July, 2015 till 2021
    names = []
    for n in list(df_rf['Matched_Names'].unique()):
        if len(df_rf[(df_rf['Matched_Names'] == n) & (df_rf["Year"] == 2015)]) == 6:
            if len(df_rf[(df_rf['Matched_Names'] == n) & (df_rf["Year"] == 2016)]) == 12:
                if len(df_rf[(df_rf['Matched_Names'] == n) & (df_rf["Year"] == 2017)]) == 12:
                    if len(df_rf[(df_rf['Matched_Names'] == n) & (df_rf["Year"] == 2018)]) == 12:
                        if len(df_rf[(df_rf['Matched_Names'] == n) & (df_rf["Year"] == 2019)]) == 12:
                            if len(df_rf[(df_rf['Matched_Names'] == n) & (df_rf["Year"] == 2020)]) == 12:
                                names.append(n)


    df_rf = df_rf[df_rf['Matched_Names'].isin(names)]

    # Summing up the occurrence number for the relevant offenses
    df_rf["Offenses_Relevant"] = df_rf[['Prostitution Offenses', 'Robbery',
                                      'Sex Offenses', 'Larceny Offenses']].sum(axis = 1)

    df_rf.drop(columns = ['Prostitution Offenses', 'Robbery', 'Sex Offenses', 'Larceny Offenses', 
                          'OccurMonth_Year'], inplace = True)
    
    return df_rf


def total_offenses(df, list_col):
    df_rf_total = df[list_col] 
    # Drop the rows with missing values
    df_rf_total.dropna(inplace = True)
    # Year and Month column being set as datetime
    df_rf_total['OccurMonth_Year'] = pd.to_datetime(df_rf_total['OccurMonth_Year'], errors='coerce')
    df_rf_total["Year"] = df_rf_total['OccurMonth_Year'].dt.year
    df_rf_total["Month"] = df_rf_total['OccurMonth_Year'].dt.month
    names = []
    for n in list(df_rf_total['Matched_Names'].unique()):
        if len(df_rf_total[(df_rf_total['Matched_Names'] == n) & (df_rf_total["Year"] == 2015)]) == 6:
            if len(df_rf_total[(df_rf_total['Matched_Names'] == n) & (df_rf_total["Year"] == 2016)]) == 12:
                if len(df_rf_total[(df_rf_total['Matched_Names'] == n) & (df_rf_total["Year"] == 2017)]) == 12:
                    if len(df_rf_total[(df_rf_total['Matched_Names'] == n) & (df_rf_total["Year"] == 2018)]) == 12:
                        if len(df_rf_total[(df_rf_total['Matched_Names'] == n) & (df_rf_total["Year"] == 2019)]) == 12:
                            if len(df_rf_total[(df_rf_total['Matched_Names'] == n) & (df_rf_total["Year"] == 2020)]) == 12:
                                names.append(n)
    df_rf_total = df_rf_total[df_rf_total['Matched_Names'].isin(names)]
    df_rf_total.drop(columns = ['OccurMonth_Year'], inplace = True)
    
    return df_rf_total

def train_test_split(encoded_df, label):
    train_features = np.array(encoded_df[encoded_df["Year"].isin([2015,
                                                                    2016,
                                                                    2017,
                                                                    2018, 
                                                                    2019])].drop(label,
                                                                                 axis = 1))

    train_label = np.array(encoded_df.loc[encoded_df["Year"].isin([2015,
                                                                         2016,
                                                                         2017,
                                                                         2018,
                                                                         2019]), label])
    test_features = np.array(encoded_df[encoded_df["Year"] == 2020].drop(label, axis = 1))
    test_label = np.array(encoded_df.loc[encoded_df["Year"] == 2020, label])

    return train_features, train_label, test_features, test_label
