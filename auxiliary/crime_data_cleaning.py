import os
import pandas as pd
import datetime


# Catch and ignore the warnings
import warnings
warnings.filterwarnings("ignore")

##Data cleaning




def clean_data(file):

     df = []
     for f in file:
         csv_file="data"+ "/" + f
         print(csv_file)
         df.append(pd.read_csv(csv_file))
         df_full = pd.concat(df, ignore_index=True)


     data=  df_full
     #Cleaning the Dates
     data['OccurDate'] = pd.to_datetime(data['OccurDate'],format='%d/%m/%Y')
     data['OccurMonth_Year']  = pd.to_datetime(data['OccurDate']).dt.to_period('M')

     to_drop = ['Address',
               'CrimeAgainst',
               'OffenseType',
               'OpenDataLat',
               'OpenDataLon',
               'OpenDataX',
               'OpenDataY',
               'ReportDate']


     data= data[data.OccurMonth_Year>"2015-06-01"]
     data= data[data.OccurMonth_Year<"2021-06-01"]

     data.drop(to_drop, inplace=True, axis=1)
     return data