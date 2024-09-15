import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(color_codes=True)


df = pd.read_csv('Crime_Data.csv')

# sample_df = df.sample(frac=0.02, random_state = 42)
# sample_df.to_csv('sample_filed.csv', index=False)

df.drop(['Crm Cd 1','Crm Cd 2','Crm Cd 3','Crm Cd 4','Premis Cd', 'Weapon Used Cd', 'Status', 'Premis Desc'], axis=1, inplace=True)

"""
Getting the order of which areas have the most crimes
"""
area_counts = df['AREA NAME'].value_counts().reset_index()
area_counts.columns = ['AREA NAME', 'Count']
print(area_counts)

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

print(crime_counts_top_10)

print(df['Weapon Desc'].isnull().sum()) #How many crimes were committed without weapons 
print(df['Weapon Desc'].notnull().sum()) #How many crimes were committed with weapons

# sns.barplot(x='Crm Cd Desc', y='Count', data=crime_counts_top_10)
# plt.xticks(rotation=90)
# plt.title('Count of Entries Group by Crime Description (Top 10)')
# plt.xlabel('Crm Cd Desc')
# plt.ylabel('Count')
# plt.show()