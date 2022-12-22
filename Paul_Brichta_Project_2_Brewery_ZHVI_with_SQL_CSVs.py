#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import dependencies
import json
import requests
from pprint import pprint
import pandas as pd


# In[2]:


# Establish the query url from openbrewery.org
query_url = "https://api.openbrewerydb.org/breweries?"


# In[3]:


# Set up a list to hold reponse info
breweries = []

# Loop through all of the pages to get all of the brewery data (limit 50 per page)
for page in range(1, 165):
    response = requests.get(query_url + f"page={page}&per_page=50").json()
    breweries.append(response)


# In[4]:


# Print the data to see what we are working with
# We can see the data comes back as a list of lists of dictionaries
# Each list inside the main list contains the info from 50 breweries 
# pprint(breweries[1])
# pprint(breweries[2])


# In[5]:


# Chris helped me with this to get the data into a single list of dictionaries
breweries_single_list = [item for sublist in breweries for item in sublist]
# breweries_single_list


# In[6]:


# Create a data frame from the list of dictionaries that contains all the brewery information
brewery_df = pd.DataFrame(breweries_single_list)
# brewery_df


# In[7]:


# Filter out the breweries not in the United States
brewery_us = brewery_df.loc[brewery_df["country"] == "United States"].copy()
# brewery_us


# In[8]:


# First step to fix postal code results - eliminate the hyphen
brewery_us["zipcode_fix1"] = brewery_us.postal_code.str.replace('-', '')


# In[9]:


# Second step to fix postal code results - take first 5 digits of the postal code eliminating the last 4 which we do not need
brewery_us["zipcode_fix2"] = brewery_us["zipcode_fix1"].str[:5]


# In[10]:


# Replace the postal_code column with the fixed zipcodes
brewery_us['postal_code'] = pd.to_numeric(brewery_us['zipcode_fix2'])
# brewery_us.columns


# In[11]:


# Use only the columns we desire and drop the rest from the data frame
brewery_us_zipcode_df = brewery_us[['id', 'name', 'brewery_type', 'street', 'city', 'state', 'postal_code', 'country', 'longitude', 'latitude', 'phone', 'website_url']]
# brewery_us_zipcode_df


# In[12]:


# Reset the index values for the data frame
brewery_us_zipcode_df = brewery_us_zipcode_df.reset_index(drop = True)
# brewery_us_zipcode_df


# In[13]:


# Store the Zillow Home Value Index data filepath in a variable
zhvi_data = "ResourcesPB/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"


# In[14]:


# Create a data frame from the Zillow Home Value Index data csv file
zhvi_df = pd.read_csv(zhvi_data)
# zhvi_df.columns


# In[15]:


# Use only the columns we desire, rename and drop the rest of the columns from the data frame
zhvi_df = zhvi_df[['RegionName', 'CountyName', '2022-11-30']].rename(columns={'RegionName':'postal_code', 'CountyName':'county', '2022-11-30':'ZHVI'})
# zhvi_df


# In[16]:


# Merge the two data frames on postal_code
brewery_zhvi_df = brewery_us_zipcode_df.merge(zhvi_df, how='right', on='postal_code')
# brewery_zhvi_df.head()


# In[17]:


# Rename the street column to address
brewery_zhvi_df = brewery_zhvi_df.rename(columns={'street':'address'})
# brewery_zhvi_df


# In[18]:


# Create a csv file of the merged data
brewery_zhvi_df.to_csv("ResourcesPB/merged_brewery_zhvi.csv", index = False)


# Create CSVs of all of the brewery and home value information to import into an SQL database

# In[22]:


# Create a csv of the idenifying information of all of the breweries
brewery_id_df = brewery_zhvi_df[['id', 'name', 'brewery_type']]
brewery_id_df.dropna(subset=['id'], inplace=True)
brewery_id_df.to_csv("ResourcesPB/brewery_id.csv", index=False)


# In[23]:


# Create a csv of the address information of all of the breweries
brewery_address_df = brewery_zhvi_df[['id', 'address', 'city', 'state', 'postal_code', 'country']]
brewery_address_df.dropna(subset=['id'], inplace=True)
brewery_address_df.to_csv("ResourcesPB/brewery_address.csv", index=False)


# In[24]:


# Create a csv of the location information of all of the breweries
brewery_location_df = brewery_zhvi_df[['id', 'longitude', 'latitude']]
brewery_location_df.dropna(subset=['id'], inplace=True)
brewery_location_df.to_csv("ResourcesPB/brewery_location.csv", index=False)


# In[25]:


# Create a csv of the contact information of all of the breweries
brewery_contact_df = brewery_zhvi_df[['id', 'phone', 'website_url']]
brewery_contact_df.dropna(subset=['id'], inplace=True)
brewery_contact_df.to_csv("ResourcesPB/brewery_contact.csv", index=False)


# In[29]:


# Create a csv of the Zillow Home Value Index information of all of the postal codes
zhvi_df.to_csv("ResourcesPB/brewery_zhvi.csv", index=False)

