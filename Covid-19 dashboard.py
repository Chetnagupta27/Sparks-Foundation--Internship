#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os 
import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from math import sqrt
from datetime import datetime

get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:



raw_data_confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
raw_data_deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
raw_data_Recovered = pd.read_csv('time_series_covid19_recovered_global.csv')

print("The Shape of confirmed is: ", raw_data_confirmed.shape)
print("The Shape of deaths is: ", raw_data_deaths.shape)
print("The Shape of recovered is: ", raw_data_Recovered.shape)

raw_data_confirmed.head()


# Un-Pivoting the data

# In[6]:


raw_data_confirmed2 = pd.melt(raw_data_confirmed, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                              var_name=['Date'])
raw_data_deaths2 = pd.melt(raw_data_deaths, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                           var_name=['Date'])
raw_data_Recovered2 = pd.melt(raw_data_Recovered, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                              var_name=['Date'])


print("The Shape of Confirmed is: ", raw_data_confirmed2.shape)
print("The Shape of deaths is: ", raw_data_deaths2.shape)
print("The Shape of recovered is: ", raw_data_Recovered2.shape)


raw_data_confirmed2


# In[7]:


raw_data_confirmed2.head()


# Converting the new column to dates
# 

# In[9]:


raw_data_confirmed2['Date'] = pd.to_datetime(raw_data_confirmed2['Date'])
raw_data_deaths2['Date'] = pd.to_datetime(raw_data_deaths2['Date'])
raw_data_Recovered2['Date'] = pd.to_datetime(raw_data_Recovered2['Date'])


# Renaming the Values

# In[10]:


raw_data_confirmed2.columns = raw_data_confirmed2.columns.str.replace('value', 'Confirmed')
raw_data_deaths2.columns = raw_data_deaths2.columns.str.replace('value', 'Deaths')
raw_data_Recovered2.columns = raw_data_Recovered2.columns.str.replace('value', 'Recovered')


# In[11]:


raw_data_confirmed2.head()


# Investigating the NULL values

# In[12]:


raw_data_Recovered2.isnull().sum()


# Dealing with NULL values

# In[14]:


raw_data_confirmed2['Province/State'].fillna(raw_data_confirmed2['Country/Region'], inplace=True)
raw_data_deaths2['Province/State'].fillna(raw_data_deaths2['Country/Region'], inplace=True)
raw_data_Recovered2['Province/State'].fillna(raw_data_Recovered2['Country/Region'], inplace=True)


# In[15]:


raw_data_Recovered2.isnull().sum()


# printing shapes before the join

# In[16]:



print("The Shape of confirmed is: ", raw_data_confirmed2.shape)
print("The Shape of deaths is: ", raw_data_deaths2.shape)
print("The Shape of recovered is: ", raw_data_Recovered2.shape)


# In[17]:


raw_data_confirmed2


# In[18]:


full_join = raw_data_confirmed2.merge(raw_data_deaths2[['Province/State','Country/Region','Date','Deaths']], 
                                      how = 'left', 
                                      left_on = ['Province/State','Country/Region','Date'], 
                                      right_on = ['Province/State', 'Country/Region','Date'])
full_join.head()


# In[19]:


full_join = full_join.merge(raw_data_Recovered2[['Province/State','Country/Region','Date','Recovered']], 
                                      how = 'left', 
                                      left_on = ['Province/State','Country/Region','Date'], 
                                      right_on = ['Province/State', 'Country/Region','Date'])
full_join.head()


# Adding Month and Year as a new Column

# In[20]:


full_join['Month-Year'] = full_join['Date'].dt.strftime('%b-%Y')


# In[21]:



full_join.head()


# In[22]:


full_join2 = full_join.copy()

#creating a new date columns - 1
full_join2['Date - 1'] = full_join2['Date'] + pd.Timedelta(days=1)
full_join2.rename(columns={'Confirmed': 'Confirmed - 1', 'Deaths': 'Deaths - 1', 'Recovered': 'Recovered - 1',
                          'Date': 'Date Minus 1'}, inplace=True)


# In[23]:


full_join2.head()


# In[24]:


full_join3 = full_join.merge(full_join2[['Province/State', 'Country/Region','Confirmed - 1', 'Deaths - 1', 
                            'Recovered - 1', 'Date - 1', 'Date Minus 1']], how = 'left',
                             left_on = ['Province/State','Country/Region','Date'], 
                             right_on = ['Province/State', 'Country/Region','Date - 1'])
full_join3.head()


# In[25]:



full_join3['Confirmed Daily'] = full_join3['Confirmed'] - full_join3['Confirmed - 1']
full_join3['Deaths Daily'] = full_join3['Deaths'] - full_join3['Deaths - 1']
full_join3['Recovered Daily'] = full_join3['Recovered'] - full_join3['Recovered - 1']

print(full_join3.shape)


# In[26]:



full_join3.head()


# In[27]:


#creating a new df    
full_join2 = full_join.copy()

#creating a new date columns - 1
full_join2['Date - 1'] = full_join2['Date'] + pd.Timedelta(days=1)
full_join2.rename(columns={'Confirmed': 'Confirmed - 1', 'Deaths': 'Deaths - 1', 'Recovered': 'Recovered - 1',
                          'Date': 'Date Minus 1'}, inplace=True)

#Joing on the 2 DFs
full_join3 = full_join.merge(full_join2[['Province/State', 'Country/Region','Confirmed - 1', 'Deaths - 1', 
                            'Recovered - 1', 'Date - 1', 'Date Minus 1']], how = 'left',
                             left_on = ['Province/State','Country/Region','Date'], 
                             right_on = ['Province/State', 'Country/Region','Date - 1'])

#minus_onedf.rename(columns={'Confirmed': 'Confirmed - 1', 'Deaths': 'Deaths - 1', 'Recovered': 'Recovered - 1'}, inplace=True)

full_join3.head()

# Additional Calculations
full_join3['Confirmed Daily'] = full_join3['Confirmed'] - full_join3['Confirmed - 1']
full_join3['Deaths Daily'] = full_join3['Deaths'] - full_join3['Deaths - 1']
full_join3['Recovered Daily'] = full_join3['Recovered'] - full_join3['Recovered - 1']

print(full_join3.shape)


# In[28]:


full_join3.head()


# In[29]:


# Additing manually the numbers for first day

full_join3['Confirmed Daily'].loc[full_join3['Date'] == '2020-01-22'] = full_join3['Confirmed']
full_join3['Deaths Daily'].loc[full_join3['Date'] == '2020-01-22'] = full_join3['Deaths']
full_join3['Recovered Daily'].loc[full_join3['Date'] == '2020-01-22'] = full_join3['Recovered']

# deleting columns
del full_join3['Confirmed - 1']
del full_join3['Deaths - 1']
del full_join3['Recovered - 1']
del full_join3['Date - 1']
del full_join3['Date Minus 1']


# In[30]:


full_join3[full_join3["Deaths Daily"]<0]


# In[31]:


full_join3['Deaths Daily']=np.where(full_join3['Deaths Daily']<0 ,0,full_join3['Deaths Daily'])


# In[34]:


full_join3['Confirmed Daily']=np.where(full_join3['Confirmed Daily']<0 ,0,full_join3['Confirmed Daily'])


# In[35]:


full_join3['Recovered Daily']=np.where(full_join3['Recovered Daily']<0 ,0,full_join3['Recovered Daily'])


# In[39]:


path = "C:\\Users\\pc\\Desktop"

# Changing my CWD
os.chdir(path)

full_join3.to_csv('CoronaVirus Data.csv')


# In[ ]:




