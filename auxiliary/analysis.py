import numpy as np
import pandas as pd
#import statsmodels
import statsmodels.formula.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col



def corona_reg(data):


 n_month_crime_with_brightness=data


 n_month_crime_with_brightness['First_Lockdown']=0
 n_month_crime_with_brightness.loc[(n_month_crime_with_brightness['OccurMonth_Year']>="2020-03") & (n_month_crime_with_brightness['OccurMonth_Year']<="2020-07"),'First_Lockdown'] =1
 n_month_crime_with_brightness[n_month_crime_with_brightness['commute_by_walking_perc'].isnull()]

 #n_month_crime_with_brightness['Total_Offenses']= np.log(n_month_crime_with_brightness['Total_Offenses'])
 #n_month_crime_with_brightness['median_household_income']= np.log(n_month_crime_with_brightness['median_household_income'])

 np.seterr(divide = 'ignore')

 n_month_crime_with_brightness['log_median_household_income']=  np.where(n_month_crime_with_brightness['median_household_income']>0,np.log(n_month_crime_with_brightness['median_household_income']), 0)
 n_month_crime_with_brightness['log_Total_Offenses'] = np.where(n_month_crime_with_brightness['Total_Offenses']>0, np.log(n_month_crime_with_brightness['Total_Offenses']), 0)

 ols_1 = sm.ols(formula='log_Total_Offenses ~ First_Lockdown',
                          data=n_month_crime_with_brightness).fit()
 ols_2 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_3 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown  + log_median_household_income',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_4 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown + log_median_household_income + people_below_poverty',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_5 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown + log_median_household_income + unemployed_perc + people_below_poverty',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_6 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown + log_median_household_income + unemployed_perc + people_below_poverty + perc_diff_state_last_year + total_newcomers_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()


 ols_7 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown + log_median_household_income + unemployed_perc + people_below_poverty + perc_diff_state_last_year + total_newcomers_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_8 =  smf.mixedlm('log_Total_Offenses ~ First_Lockdown + log_median_household_income + unemployed_perc + people_below_poverty +  perc_diff_state_last_year + commute_by_walking_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()




 reg1 = ols_1
 reg2 = ols_2
 reg3 = ols_3
 reg4 = ols_4
 reg5 = ols_5
 reg6 = ols_6
 reg7 = ols_7
 reg8 = ols_8


 results = summary_col([reg1, reg2, reg3, reg4,reg5,reg6,reg7,reg8],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)', 'Model\n(3)',  'Model\n(4)', 
                               'Model\n(5)',  'Model\n(6)',  'Model\n(7)' , 'Model\n(8)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})
 return(results)





def crime_reg(data):

 pd.options.mode.chained_assignment = None 
 n_month_crime_with_brightness=data

 n_month_crime_with_brightness=n_month_crime_with_brightness[n_month_crime_with_brightness['Average Radiance Per Pixel Per month'].notnull()]


 np.seterr(divide = 'ignore')
 n_month_crime_with_brightness['log_median_household_income']=  np.where(n_month_crime_with_brightness['median_household_income']>0,np.log(n_month_crime_with_brightness['median_household_income']), 0)
 n_month_crime_with_brightness['log_Total_Offenses'] = np.where(n_month_crime_with_brightness['Total_Offenses']>0,  np.log(n_month_crime_with_brightness['Total_Offenses']), 0)
 n_month_crime_with_brightness['log_brightness'] = np.where(n_month_crime_with_brightness['Average Radiance Per Pixel Per month']>0,  np.log(n_month_crime_with_brightness['Average Radiance Per Pixel Per month']), 0)
 n_month_crime_with_brightness['night_brightness'] = n_month_crime_with_brightness['Average Radiance Per Pixel Per month']



 ols_1 = sm.ols(formula='log_Total_Offenses ~ night_brightness-1',
                          data=n_month_crime_with_brightness).fit()

 ols_2 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_3 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1  + log_median_household_income',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_4 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1 + log_median_household_income + people_below_poverty',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_5 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_6 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty + perc_diff_state_last_year + total_newcomers_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()


 ols_7 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty + perc_diff_state_last_year + total_newcomers_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_8 =  smf.mixedlm('log_Total_Offenses ~ night_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty +  perc_diff_state_last_year + commute_by_walking_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_9 =  smf.mixedlm('log_Total_Offenses ~ log_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_10 =  smf.mixedlm('log_Total_Offenses ~ log_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty + perc_diff_state_last_year + total_newcomers_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()


 ols_11=  smf.mixedlm('log_Total_Offenses ~ log_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty + perc_diff_state_last_year + total_newcomers_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()

 ols_12 =  smf.mixedlm('log_Total_Offenses ~ log_brightness-1 + log_median_household_income + unemployed_perc + people_below_poverty +  perc_diff_state_last_year + commute_by_walking_perc',n_month_crime_with_brightness, groups=n_month_crime_with_brightness["Neighborhood"]).fit()




 reg1 = ols_1
 reg2 = ols_2
 reg3 = ols_3
 reg4 = ols_4
 reg5 = ols_5
 reg6 = ols_6
 reg7 = ols_7
 reg8 = ols_8
 reg9 = ols_9
 reg10 = ols_10
 reg11 = ols_11
 reg12 = ols_12

 results = summary_col([reg1, reg2, reg3, reg4,reg5,reg6,reg7,reg8,reg9,reg10,reg11,reg12],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)', 'Model\n(3)',  'Model\n(4)', 
                               'Model\n(5)',  'Model\n(6)',  'Model\n(7)' , 'Model\n(8)', 'Model\n(9)', 'Model\n(10)'
                              , 'Model\n(11)', 'Model\n(12)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})
 return(results)


