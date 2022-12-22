#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""importing libraries"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


# In[ ]:


## Importing Data. 


# In[2]:


df_india = pd.read_csv("C:/Users/kamle/Downloads/archive/covid_19_india.csv")
df_india


# In[ ]:


## Getting familiar with Data


# In[3]:


"Checking the range of data"

df_india.shape


# In[4]:


"Getting information about Data type and non-null values"

df_india.info()


# In[5]:


"Getting numeric column detials "

df_india.describe()


# In[6]:


"Getting information of null values in Dataset"

df_india.isna().sum()


# In[ ]:


###  Note: There is no null value's in dataset


# In[7]:


"finding unique values from 'State/UnionTerritory' column"

df_india['State/UnionTerritory'].unique(),df_india['State/UnionTerritory'].nunique()


# In[66]:


"Correcting spelling mistakes or impurities"

state_correction_dict = {
    'Bihar****':'Bihar',
    'Dadra and Nagar Haveli':'Dadra and Nagar Haveli and Daman and Diu',
    'Madhya Pradesh***':'Madhya Pradesh',
    'Maharashtra***':'Maharashtra',
    'Karanataka':'Karnataka'
}

def state_correction(state):
    try:
        return state_correction_dict[state]
    except:
        return state
    
df_india['State/UnionTerritory'] = df_india['State/UnionTerritory'].apply(state_correction)
df_india['State/UnionTerritory'].nunique()


# In[ ]:


### Note: Here we have corrected spelling mistakes in columns.


# In[9]:


"Changing the format of date"

df_india['Date'] = pd.to_datetime(df_india['Date'])
df_india['Date'] = df_india['Date'].dt.strftime('%d-%m-%Y')
df_india['Date']


# In[10]:


"Removing unwanted columns from dataset using 'drop'."

df_india.drop(['Time','ConfirmedIndianNational','ConfirmedForeignNational'],axis = 1,inplace = True)
df_india


# In[11]:


"Getting only Numeric columns"

num = df_india.select_dtypes(exclude = object)
num


# In[12]:


"Getting only categorical data"

obj = df_india.select_dtypes(include = object)
obj


# In[ ]:


## Data Manipulation 


# In[13]:


"Identifying active cases , We counted the values by using values in confirmed, cured, deaths column"

df_india['Active'] = df_india['Confirmed'] - df_india['Cured'] - df_india['Deaths']
df_india


# In[ ]:


### Note: We can now check the active cases in each state


# In[14]:


"using pivot function to find cured , deaths , confirmed cases State wise"

statewise = pd.pivot_table(df_india,values=['Cured','Deaths','Confirmed'],index='State/UnionTerritory',aggfunc='max',margins=True)
statewise


# In[93]:


"Top 10 states with Active cases"

df_top_10 = df_india.nlargest(10,['Active'])

df_top_10 = df_india.groupby(['State/UnionTerritory'])['Active'].max().sort_values(ascending=False).reset_index()
df_top = df_top_10.nlargest(10,['Active'])
df_top


# In[132]:


"Top 10 states with deaths cases"

df_deaths_10 = df_india.nlargest(10,['Deaths'])

df_deaths_10 = df_india.groupby(['State/UnionTerritory'])['Deaths'].max().sort_values(ascending=False).reset_index()
df_deaths = df_deaths_10.nlargest(10,['Deaths'])

df_deaths


# In[17]:


"Finding recovery rate and deathrate"

statewise['Recoveryrate'] = statewise['Cured']*100/statewise['Confirmed']
statewise['Deathrate'] = statewise['Deaths']*100/statewise['Confirmed']
statewise


# In[18]:


"Correlation amongs the columns"

statewise.corr()


# In[ ]:


## Data visualization


# In[19]:


"""Barplot for Confirmed , Deaths , Cured , Active"""
fig = plt.figure(figsize=(20,10))

confirm= df_india['Confirmed'].sum()
cured = df_india['Cured'].sum()
deaths= df_india['Deaths'].sum()
active= df_india['Active'].sum()

print('Total Confirmed cases =',confirm)
print('Total Cured cases =',cured)
print('Total Active cases =',active)
print('Total Death cases =',deaths)

barplot = sns.barplot(x=['Confirmed','Cured','Deaths','active'],y=[confirm,cured,deaths,active])
barplot.set_yticklabels(labels=(barplot.get_yticks()*1).astype(int))

plt.show()


# In[103]:


"Piechart for 'Confirmed','Cured',Deaths & 'Active'"

fig = plt.figure(figsize=(17,10))
df_values = [df_india['Confirmed'].sum(),df_india['Cured'].sum(),df_india['Deaths'].sum(),df_india['Active'].sum()]
df_keys = [confirm,cured,deaths,active]


plt.pie(df_keys,labels = df_keys, explode = (0.02,0.02,0.1,0.02), autopct = '%.0f%%')
plt.legend(['Confirmed','Cured','Deaths','Active'])


# In[107]:


"Pie Chart Of 10 Top states with Active Cases"

fig = plt.figure(figsize=(17,10))
df_top.groupby(["State/UnionTerritory"]).sum()["Active"].plot(kind='pie',rot=90,explode=(0.05,0.02,0.03,0.04,0.04,0.05,0.1,0.04,0.09,0.04),autopct='%1.0f%%')
plt.title('Top 10 states with Active cases',size=20)
plt.show()
  


# In[52]:


"Bar Plot Of Top 10 Active Cases"

fig = plt.figure(figsize=(20,10))
sns.barplot(data = df_top.iloc[:10],y='Active',x='State/UnionTerritory')
plt.title('Top 10 states with Most Active cases', size=20)
plt.show()


# In[ ]:


## Note : As per above visual's it is clear that Maharashtra has maximum number of Active cases wheras Chhattisgarh has the least number of Active cases.


# In[134]:


"""Pie chart of top 10 states with death cases"""

fig = plt.figure(figsize=(17,10))
df_deaths.groupby(["State/UnionTerritory"]).sum()["Deaths"].plot(kind='pie',rot=90,explode=(0.05,0.02,0.03,0.04,0.04,0.05,0.1,0.04,0.09,0.04),autopct='%1.0f%%')
plt.title("Pie chart of top 10 states with death cases",size = 20)


# In[114]:


"Bar graph with top 10 states with most Death cases"


df_deaths = df_india.groupby('State/UnionTerritory').max()[['Deaths','Date']].sort_values(by='Deaths',ascending=False).reset_index()
fig = plt.figure(figsize=(20,10))
plot1 = sns.barplot(data = df_deaths.iloc[:10],y='Deaths',x='State/UnionTerritory')
plt.title('Top 10 states with most death cases', size=20)
plt.xlabel('states')
plt.ylabel('Deaths')
plt.show()


# In[ ]:


## Note : As per above visual's it is clear that Maharashtra has most number of death cases and Chhattisgarh has least number of death cases.


# In[91]:


" Top 5 Most affected states"

fig = plt.figure(figsize=(15,10))
plot = sns.lineplot(data = df_india[df_india['State/UnionTerritory'].isin(['Maharashtra','Karnataka','Tamil Nadu','Delhi','Uttar Pradesh'])],x='Date',y='Active',hue = 'State/UnionTerritory',size='State/UnionTerritory')
plt.title('5 most affected states',size=20)
plt.show()


# In[ ]:


## correlation Heatmap


# In[85]:


"Correlation Heatmap"

fig = plt.figure(figsize=(15,10))
sns.heatmap(df_india.corr(),cmap="Blues")
plt.title('Correlation Heatmap',size=20)
plt.show()


# In[90]:


"Fatality ratio of contaminated states"

df_india['Fatality_ratio']= df_india['Deaths']/df_india['Confirmed']
a4_dims = (15,7)
fig,ax = plt.subplots(figsize=a4_dims)
sns.pointplot(data = df_india,x='State/UnionTerritory',y='Fatality_ratio',ax=ax,color='Green')
plt.xticks(rotation=90)
plt.title('Fatality ratio of contaminated states',size=20)
plt.show()

