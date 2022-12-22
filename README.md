<h1> Project-2: Extract Transform Load </h1>
<h3>  </h3>

For this project we decided to investigate if home value has any correlation to brewery location.

The brewery API data we used is from a free, open databse containing brewery information from around the world. The data retrieved from the API call included brewery id, name, brewery type, address, city, state, postal code, country, longitude, latitude, phone, and website url.

According to openbrewery.org the data set was last updated in October 2022.

https://www.openbrewerydb.org/documentation
<hr />

The home value information was retrieved from Zillow.
Zillow publishes housing data on their website by organinzing it by Data Type and Geography.
The dataset we used contained the Zillow Home Value Index (ZHVI) smoothed and seasonally adjusted.
The CSV contained the ZHVI information by month beginning in January 2000.
Since we only care about the current values of homes we decided to use the postal code, county, and ZHVI data from 11/30/2022 from Zillow.

https://www.zillow.com/research/data/
<hr />

The ZHVI data csv contained information from many more postal codes than the brewery data allowing us to gather information about areas that have breweries and areas that do not have breweries.

By combining the Brewery data with Zillow Home Value Index data we can look further into questions like:
<ol>
  <li>Is the number of breweries correlated with home values in the same zipcode?
  <li>Is the number of breweries correlated with states that have legalized other recreational drugs?
  <li>Does home value differ in areas that contain breweries and in areas without breweries?
</ol>

Overall the data can be used to target specific groups and areas that would be more receptive to having breweries nearby.
Targeting areas with higher home values could lead to a more successful brewery business.


Data extraction:

The Openbrewery data was obtained by querying the api https://api.openbrewerydb.org.  Due to a limitation of the api, the data was pulled in 50 record batches, for a total of 164 api calls.
The api data was stored in a list of dictonaries which was used to create a pandas DataFrame.
This raw data was saved to the Resources folder as "breweries_all_rawdata.csv".

The Zillow data was obtained by downloading a CSV file from https://www.zillow.com/research/data/ page under Zillow Home Value Index (ZHVI) section with the selections Data Type "ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted($)" and Geography "Zip Code".

Data Transformation:

Data Loading (Mongo database):

Data Loading (SQL database):

The Openbrewery data 




**Credit:**
- Chris Gruenhagen
- Paul Brichta

December 2022
