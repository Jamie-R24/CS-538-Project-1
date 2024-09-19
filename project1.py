import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
sns.set(color_codes=True)


df = pd.read_csv('Crime_Data.csv')
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# sample_df = df.sample(frac=0.02, random_state = 42)
# sample_df.to_csv('sample_filed.csv', index=False)

df.drop(['Crm Cd 1','Crm Cd 2','Crm Cd 3','Crm Cd 4','Premis Cd', 'Weapon Used Cd', 'Status', 'Premis Desc'], axis=1, inplace=True)

"""
Getting the order of which areas have the most crimes
"""
area_counts = df['AREA NAME'].value_counts().reset_index()
area_counts.columns = ['AREA NAME', 'Count']
# print(area_counts)

# sns.barplot(x='AREA NAME', y='Count', data=area_counts)
# plt.xticks(rotation=90)
# plt.title('Count of Entries Group by Area Name')
# plt.xlabel('Area Name')
# plt.ylabel('Count')
# plt.show()

"""
Getting the Top 10 most committed crimes from the dataset
"""
crime_counts = df['Crm Cd Desc'].value_counts().reset_index()
crime_counts.columns = ['Crm Cd Desc', 'Count']
crime_counts_top_10 = crime_counts.nlargest(10, 'Count')

# print(crime_counts_top_10)

# print('\nCrimes committed without weapons: %d' % df['Weapon Desc'].isnull().sum()) #How many crimes were committed without weapons 
# print('Crimes committed with weaopns: %d' % df['Weapon Desc'].notnull().sum()) #How many crimes were committed with weapons

# print('\n')

# sns.barplot(x='Crm Cd Desc', y='Count', data=crime_counts_top_10)
# plt.xticks(rotation=90)
# plt.title('Count of Entries Group by Crime Description (Top 10)')
# plt.xlabel('Crm Cd Desc')
# plt.ylabel('Count')
# plt.show()

#-------------------------------------------
#---------------- Task 3 -------------------
#-------------------------------------------

top_five_crime_stats = df[df['Crm Cd Desc'].isin(['VEHICLE - STOLEN', 'BATTERY - SIMPLE ASSAULT', 'BURGLARY FROM VEHICLE', 'THEFT OF IDENTITY', 'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)'])].copy()
top_five_crime_stats['DATE OCC'] = pd.to_datetime(top_five_crime_stats['DATE OCC'], errors = 'coerce')
top_five_crime_stats['Year'] = top_five_crime_stats['DATE OCC'].dt.year
top_five_crime_stats = top_five_crime_stats[top_five_crime_stats['Year'] < 2024]
yearly_trends = top_five_crime_stats.groupby(['Year', 'Crm Cd Desc']).size().reset_index(name='Count')

vehicle_stolen_stats = df[df['Crm Cd Desc'] == 'VEHICLE - STOLEN'].copy()
vehicle_stolen_stats['DATE OCC'] = pd.to_datetime(vehicle_stolen_stats['DATE OCC'], errors = 'coerce')
vehicle_stolen_stats['Year'] = vehicle_stolen_stats['DATE OCC'].dt.year
vehicle_stolen_stats = vehicle_stolen_stats[vehicle_stolen_stats['Year'] < 2024]
#yearly_trends = vehicle_stolen_stats.groupby('Year').size().reset_index(name='Count')

# plt.figure(figsize=(10,0))
# sns.lineplot(data=yearly_trends, x='Year', y='Count', hue='Crm Cd Desc', marker='o')
# plt.title('Yearly Trend of Top 5 Crime Descriptions')
# plt.xlabel('Year')
# plt.ylabel('Number of Cases')
# plt.xticks(yearly_trends['Year'].unique())
# plt.grid(True)
# plt.show()

identity_theft_stats = df[df['Crm Cd Desc'] == 'THEFT OF IDENTITY'].copy()
identity_theft_stats['DATE OCC'] = pd.to_datetime(identity_theft_stats['DATE OCC'], errors = 'coerce')
identity_theft_stats['Year'] = identity_theft_stats['DATE OCC'].dt.year
identity_theft_stats = identity_theft_stats[identity_theft_stats['Year'] < 2024]
identity_theft_yearly_trends = identity_theft_stats.groupby('Year').size().reset_index(name='Count')

# plt.figure(figsize=(10,0))
# sns.lineplot(data=identity_theft_yearly_trends, x='Year', y='Count', marker='o')
# plt.title('Yearly Trend of Identity Theft')
# plt.xlabel('Year')
# plt.ylabel('Number of Cases')
# plt.xticks(yearly_trends['Year'].unique())
# plt.grid(True)
# plt.show()

"""
Generating a Heat Map with Lat and Lon
"""
# heatmap_df = df.dropna(subset = ['LAT', 'LON']).copy()

# map_center = [heatmap_df['LAT'].mean(), heatmap_df['LON'].mean()]
# crime_map = folium.Map(location = map_center, zoom_start=12)

# heat_data = [[row['LAT'], row['LON']] for index, row in heatmap_df.iterrows()]

# HeatMap(heat_data).add_to(crime_map)
# crime_map.save('crime_map.html')
# crime_map

# #Just the #1 Crime of Stolen Vehicles Heat Map
# vehicle_stolen_heatmap = heatmap_df.copy()
# vehicle_stolen_heatmap = vehicle_stolen_heatmap[vehicle_stolen_heatmap['Crm Cd Desc'] == 'VEHICLE - STOLEN']
# vehicle_map_center = [vehicle_stolen_heatmap['LAT'].mean(), vehicle_stolen_heatmap['LON'].mean()]
# vehicle_map = folium.Map(location = vehicle_map_center, zoom_start=12)

# vehicle_heat_data = [[row['LAT'], row['LON']] for index, row in vehicle_stolen_heatmap.iterrows()]
# HeatMap(vehicle_heat_data).add_to(vehicle_map)
# vehicle_map.save('vehicle_crime_heat_map.html')
# vehicle_map

#Analyzing Victim Age and Sex
# age_sex_df = df.dropna(subset=['Vict Age', 'Vict Sex']).copy()
# age_sex_df = age_sex_df[age_sex_df['Vict Sex'].isin(['M', 'F'])]

# age_bins= [0, 10, 18, 25, 35, 45, 55, 65, 100]
# age_labels = ['0-10', '10-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
# age_sex_df['Age Group'] = pd.cut(age_sex_df['Vict Age'], bins=age_bins, labels=age_labels, right=False)

# age_gender_counts = age_sex_df.groupby(['Age Group', 'Vict Sex'], observed=False).size().unstack(fill_value = 0)

# age_groups = age_gender_counts.index
# men_counts = age_gender_counts['M'] 
# women_counts = age_gender_counts['F']
# bar_width = 0.35 
# index = np.arange(len(age_groups)) 

# fig, ax = plt.subplots(figsize=(10, 6))
# bars1 = ax.bar(index, men_counts, bar_width, label='Men', color='blue')
# bars2 = ax.bar(index + bar_width, women_counts, bar_width, label='Women', color='red')

# ax.set_xlabel('Age Groups')
# ax.set_ylabel('Number of Victims')
# ax.set_title('Number of Male and Female Victims in Each Age Group')
# ax.set_xticks(index + bar_width/2)
# ax.set_xticklabels(age_groups)
# ax.legend()

# #This is for labeling the values so you don't have to guess and look at the y axis
# for bar in bars1:
#     ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height(), f'{int(bar.get_height())}', 
#             ha='center', va='bottom')

# for bar in bars2:
#     ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height(), f'{int(bar.get_height())}', 
#             ha='center', va='bottom')

# plt.show()


#-------------------------------------------
#---------------- Task 4 -------------------
#-------------------------------------------

weapons = df['Weapon Desc'].value_counts().reset_index().copy()
weapons.columns = ['Weapon Desc', 'Count']
top_5_weapons = weapons.nlargest(5, 'Count')

# sns.barplot(x='Weapon Desc', y='Count', data=top_5_weapons)
# plt.xticks(rotation=90)
# plt.title('Count of Entries Grouped by Weapon')
# plt.xlabel('Weapon Desc')
# plt.ylabel('Count')
# plt.show()

top_5_crimes_weapon = df[df['Crm Cd Desc'].isin(['VEHICLE - STOLEN', 'BATTERY - SIMPLE ASSAULT', 'BURGLARY FROM VEHICLE', 'THEFT OF IDENTITY', 'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)'])].copy()
top_5_crimes_weapon = top_5_crimes_weapon[top_5_crimes_weapon['Weapon Desc'] == 'STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)']
top_5_crimes_weapon['DATE OCC'] = pd.to_datetime(top_5_crimes_weapon['DATE OCC'], errors = 'coerce')
top_5_crimes_weapon['Year'] = top_5_crimes_weapon['DATE OCC'].dt.year
top_5_crimes_weapon = top_5_crimes_weapon[top_5_crimes_weapon['Year'] < 2024]
yearly_trends_weapons_crimes = top_5_crimes_weapon.groupby(['Year', 'Crm Cd Desc']).size().reset_index(name='Count')

# print(yearly_trends_weapons_crimes)

# plt.figure(figsize=(10,0))
# sns.lineplot(data=yearly_trends_weapons_crimes, x='Year', y='Count', hue='Crm Cd Desc', marker='o')
# plt.title('Yearly Trend of Top 5 Crime Descriptions')
# plt.xlabel('Year')
# plt.ylabel('Number of Cases')
# plt.xticks(yearly_trends_weapons_crimes['Year'].unique())
# plt.grid(True)
# plt.show()

df['TIME OCC'] = df['TIME OCC'].astype(str).str.zfill(4)
df['Hour'] = df['TIME OCC'].astype(int) // 100

hourly_crime_counts = df.groupby('Hour').size()
hourly_crime_counts = hourly_crime_counts.sort_index()

plt.figure(figsize=(10,6))
plt.bar(hourly_crime_counts.index, hourly_crime_counts.values, color='skyblue')
plt.xlabel('Hour of the Day (24-hour format)')
plt.ylabel('Number of Crimes')
plt.title('Crimes by Hour of the Day')
plt.xticks(range(0, 24)) 
plt.grid(True, axis='y')

# Show the plot
plt.tight_layout()
plt.show()