
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def day_night_crimes(data):
 """Compiles a regression table including different controls
    
 Args:
         data: A dataframe with both crime data, controls and brightness information
    
 Returns:
        A histogram plot for day/night crimes
 """

 clean_data_day_night= data.groupby(['OccurTime']).OffenseCount.sum().reset_index()
 clean_data_day_night['OffenseCount']  = (clean_data_day_night['OffenseCount'] /clean_data_day_night['OffenseCount'].sum()) * 100

 clean_data_day_night['day_or_night'] = np.where(((clean_data_day_night['OccurTime']<700) | (clean_data_day_night['OccurTime']>2000)),  'night', 'day')
 clean_data_day_night= clean_data_day_night.pivot_table(index=["OccurTime"], 
                    columns='day_or_night', 
                    values='OffenseCount').reset_index()
 clean_data_day_night= clean_data_day_night.fillna(0)
 clean_data_day_night['night']=-clean_data_day_night['night']
 #clean_data_day_night['day_or_night'] = np.where((clean_data_day_night['OccurTime']>2000), 'night', 'day')
 clean_data_day_night['night_square']=2*clean_data_day_night['night']




 #datetime.datetime.strptime(clean_data_day_night['OccurTime'],'%H%M')

 x = clean_data_day_night['OccurTime'].values.tolist()
 y1 = clean_data_day_night['day'].values.tolist()
 y2 = clean_data_day_night['night'].values.tolist()
 mycolors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']      
 columns = ['Night-Time', 'Day-Time']

 # Draw Plot 
 fig, ax = plt.subplots(1, 1, figsize=(16,9), dpi= 80)
 ax.fill_between(x, y1=y1, y2=0, label=columns[1], alpha=0.5, color=mycolors[1], linewidth=2)
 ax.fill_between(x, y1=y2, y2=0, label=columns[0], alpha=0.5, color=mycolors[0], linewidth=2)

 # Decorations
 ax.set_title('Night Time vs Day Time Offenses %', fontsize=18)
 #ax.set(ylim=[0, 30])
 ax.legend(loc='best', fontsize=12)
 plt.xticks(x[::60], fontsize=10, horizontalalignment='center')
 plt.yticks(np.arange(-3, 3, 0.5), fontsize=10)
 #plt.xlim(-10, x[-1])

 # Draw Tick lines  
 for y in np.arange(-3, 3, 0.5):    
    plt.hlines(y, xmin=0, xmax=2359, colors='black', alpha=0.3, linestyles="--", lw=0.5)
    
 ax.axvspan(700, 2000, alpha=0.5, color='orange')
 ax.axvspan(0, 700, alpha=0.5, color='darkblue')
 ax.axvspan(2000, 2400, alpha=0.5, color='darkblue')
 # Lighten borders
 plt.gca().spines["top"].set_alpha(0)
 plt.gca().spines["bottom"].set_alpha(.3)
 plt.gca().spines["right"].set_alpha(0)
 plt.gca().spines["left"].set_alpha(.3)
 plt.show()





def day_night_selected_crimes(data):
    
 """Compiles a regression table including different controls
    
 Args:
         data: A dataframe with both crime data, controls and brightness information
    
 Returns:
        A histogram plot for day/night crimes for selected crimes only
 """
    
 clean_data=data
 
 clean_data_day_night= clean_data.groupby(['OccurTime','OffenseCategory']).OffenseCount.sum().reset_index()
 clean_data_day_night= clean_data_day_night[(clean_data_day_night.OffenseCategory=="Motor Vehicle Theft") | (clean_data_day_night.OffenseCategory=="Assault Offenses") | (clean_data_day_night.OffenseCategory=="Prostitution Offenses")| (clean_data_day_night.OffenseCategory=="Homicide Offenses")] 



 clean_data_day_night= clean_data_day_night.pivot_table(index=["OccurTime"], 
                    columns='OffenseCategory', 
                    values='OffenseCount').reset_index()

 clean_data_day_night['day_or_night'] = np.where(((clean_data_day_night['OccurTime']<700) | (clean_data_day_night['OccurTime']>2000)),  'night', 'day')

 #clean_data_day_night= clean_data_day_night.pivot_table(index=["OccurTime","OffenseCategory"], 
                    #columns='day_or_night', 
                    #values=['Assault Offenses','Homicide Offenses','Motor Vehicle Theft','Prostitution Offenses']).reset_index()
 clean_data_day_night= clean_data_day_night.fillna(0)
 offences = ['Assault Offenses','Motor Vehicle Theft','Prostitution Offenses']

 for i in offences:
    clean_data_day_night[i]=(clean_data_day_night[i] /clean_data_day_night[i].sum()) * 100
    clean_data_day_night[i]=np.where(clean_data_day_night['day_or_night']=="night",-1*clean_data_day_night[i],clean_data_day_night[i])




 #datetime.datetime.strptime(clean_data_day_night['OccurTime'],'%H%M')

 x = clean_data_day_night['OccurTime'].values.tolist()
 y1 = clean_data_day_night['Assault Offenses'].values.tolist()
 y2 = clean_data_day_night['Motor Vehicle Theft'].values.tolist()
 y3 = clean_data_day_night['Prostitution Offenses'].values.tolist()

 mycolors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']      
 columns = ['Assault Offenses', 'Motor Vehicle Theft','Prostitution Offenses']

 # Draw Plot 
 fig, ax = plt.subplots(1,1, figsize=(16,9), dpi= 80)
 ax.plot(x, y1, label="",color='black', linewidth=2)
 ax.plot(x, y2, label="",color='black', linewidth=1)
 ax.plot(x, y3, label="",color='black', linewidth=1)
 ax.fill_between(x, y1=y1, y2=0, label=columns[0], alpha=1, edgecolor='black',color=mycolors[0], linewidth=3)
 ax.fill_between(x, y1=y2, y2=0, label=columns[1], alpha=0.5, edgecolor='black',color=mycolors[1], linewidth=3)
 ax.fill_between(x, y1=y3, y2=0, label=columns[2], alpha=0.5, edgecolor='black',color=mycolors[2], linewidth=3)

 # Decorations
 ax.set_title('Night Time vs Day Time Offenses %', fontsize=18)
 #ax.set(ylim=[0, 30])
 ax.legend(loc='best', fontsize=12)
 plt.xticks(x[::60], fontsize=10, horizontalalignment='center')
 plt.yticks(np.arange(-7, 7, 1), fontsize=10)
 #plt.xlim(-10, x[-1])

 # Draw Tick lines  
 for y in np.arange(-7, 7, 1):    
    plt.hlines(y, xmin=0, xmax=2359, colors='black', alpha=0.3, linestyles="--", lw=0.5)
    
 ax.axhspan(0,7, alpha=0.1, color='orange')
 ax.axhspan(0,-7, alpha=0.1, color='lightblue')
 #ax.axhspan(0, 700, alpha=0.5, color='darkblue')
 #ax.axvspan(2000, 2400, alpha=0.5, color='darkblue')
 # Lighten borders
 plt.gca().spines["top"].set_alpha(0)
 plt.gca().spines["bottom"].set_alpha(.3)
 plt.gca().spines["right"].set_alpha(0)
 plt.gca().spines["left"].set_alpha(.3)

 #plt.axvline(x=2000)
 #plt.axvline(x=700)
 plt.show()



def pop_graph(data):
 """Compiles a regression table including different controls
    
 Args:
      data: A dataframe with both crime data, controls and brightness information
    
 Returns:
       A population histogram for population across portland neighborhoods
 """
 df_with_controls=data
 # Create a new column - Year
 df_with_controls["Year"] = df_with_controls.OccurMonth_Year.astype(str).str[:-3]
 # Group by the dataset by Neighborhood and Year, and average the population for the years 2015 to 2021 by Neighborhood
 average_adj_pop_by_neighborhood = df_with_controls.groupby(["Neighborhood", "Year"])['adj_popn_pe_sq_mi'].mean().reset_index()

 # Create the figure
 fig = plt.figure(figsize = (30, 10))
 x = average_adj_pop_by_neighborhood[average_adj_pop_by_neighborhood["Year"] == "2015"]["Neighborhood"]
 y = average_adj_pop_by_neighborhood[average_adj_pop_by_neighborhood["Year"] == "2015"]['adj_popn_pe_sq_mi']
 
 # creating the bar plot
 plt.bar(x, y, color ='darkblue')
 
 plt.xlabel("Neighborhood Names", fontsize = "xx-large")
 plt.ylabel("Population", fontsize = "xx-large")
 plt.title("Average Adjusted Population per square miles by Neighborhoods in Portland", fontsize = "xx-large")
 plt.xticks(rotation = 90, fontsize = "xx-large")
 plt.show()


