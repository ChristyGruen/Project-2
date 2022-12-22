#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies and create base url
import pandas as pd
import requests
import numpy as nm
import pymongo

baseurl = 'https://api.openbrewerydb.org/breweries?'


# In[2]:


#create list of lists of dictionaries from openbrewerydb (total breweries = 8163 from website, pull 50 per page, need 164 pages)
listobrews = []

for page in range(1,165):
    url = f'{baseurl}page={page}&per_page=50'
    brews = requests.get(url).json()
    listobrews.append(brews)

listobrews


# In[3]:


#flatten list of lists of dictionaries to list of dictionaries
# https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
flatlist = [item for sublist in listobrews for item in sublist]
flatlist


# In[4]:


#check length of flat list
len(flatlist)


# In[44]:


#bring breweries data into pandas dataframe

brew_pd = pd.DataFrame(flatlist)
brew_pd.head(20)


# In[6]:


# save raw data to CSV
brew_pd.to_csv('Resources/breweries_all_rawdata.csv',index = False)


# In[47]:


#create US only df

brew_us_long = brew_pd.loc[brew_pd['country']=='United States'].copy()
brew_us_long.head(2)


# In[43]:


print(len(brew_us_long))


# In[9]:


#add zipcode to US only df, need to remove dashes before taking first five in string
brew_us_long['postal_codeish'] = brew_us_long['postal_code'].str.replace('-',"")
brew_us_long['zipcode'] = brew_us_long['postal_codeish'].str[:5]
brew_us_long['zipcode'] = pd.to_numeric(brew_us_long['zipcode'])
brew_us_long.rename(columns = {'street':'address'})
brew_us_long.head(2)


# In[10]:


#check datatypes
brew_us_long.dtypes


# In[11]:


#get column names
brew_us_long.columns


# In[12]:


#create clean dataframe
brew_us = brew_us_long[['id', 'name', 'brewery_type', 'street', 'city', 'state', 'zipcode', 'country',
       'longitude', 'latitude', 'phone', 'website_url']]
print(len(brew_us))
brew_us.head(2)


# In[13]:


#save cleandata
brew_us.to_csv('Resources/breweries_us_cleandata.csv',index = False)


# In[15]:


#read housing data from csv
housingdata = pd.DataFrame(pd.read_csv('Resources/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'))
housingdata.head(2)


# In[48]:


#create housing datatable subset with state/city/metro/county
housingdata2 = housingdata[['RegionName','State','City','Metro','CountyName','11/30/2022']].rename(columns = {'RegionName':'zipcode',"CountyName":"County","11/30/2022":'ZHVI'})
housingdata2.head(2)


# In[49]:


#check housing datatable - zipcode is int
housingdata2.dtypes


# In[50]:


# create housing datatable subset for merge
housingdata2_min = housingdata2[["zipcode","County","ZHVI"]]
print(len(housingdata2_min))
housingdata2_min.head(2)


# In[51]:


#save housingdata for merge  checked - all zipcodes are unique
housingdata2_min.to_csv('Resources/housingdata2_min.csv',index = False)


# In[52]:


#merge housing data and brewery data into a single dataframe
mergeall = pd.merge(housingdata2_min,brew_us,on='zipcode', how = 'left')
print(len(mergeall))
mergeall.head(2)


# In[54]:


# save merged, clean dataframe to csv
mergeall.to_csv('Resources/mergeall.csv',index = False)


# In[55]:


# create list of dictionaries from pd.DataFrame
banksy = mergeall.to_dict('records')
banksy


# In[56]:


#create connection to mongo and create/connect to db Proj2_ETL
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['Proj2_ETL']


# In[61]:


# drops collection if available to remove duplicates
mydb.homebrew.drop()


# In[62]:


# creates homebrew collection
mycol = mydb['homebrew']


# In[63]:


# write list of dictionaries into homebrew collection
x = mycol.insert_many(banksy)
# print(x.inserted_ids)


# In[64]:


#print list of databases
print(myclient.list_database_names())

