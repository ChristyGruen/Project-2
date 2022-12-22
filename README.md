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

----------
Loading into an SQL database

To load the data into a SQL database I created dataframes, and then exported to CSV. The CSVs contained the data I wanted to include on each specific table.
1. The table brewery_id contains the unique brewery id, name, and brewery_type.
2. The table brewery_address contains the unique brewery id, address, city, state, postal code, and country.
3. The table brewery_location contains the unique brewery id, longitude, and latitude.
4. The table brewery_contact contains the unique brewery id, phone number, and website url.
5. The table brewery_zhvi contains the postal code, county, and Zillow Home Value Index.

When importing the CSV files into the SQL database I originally ran into an error because the entire data set contained many postal codes that did not have any breweries.
By including these postal codes without breweries we could analyze things like home value where breweries were not present.
This created a problem where the primary key (id) was left blank in the areas without breweries.
I then had to go back into the python file and use the dropna() command to drop the rows where there were no breweries located.
I created new CSVs I could import that did not contain info from postal codes that did not have breweries.
This limited the first 4 tables to only the breweries.

The 5th table brewery_zvhi contains only the data from the Zillow website that lists all the ZVHI data for postal codes.
The limitation here is we cannot see if there are multiple breweries located in any postal code.

The primary key (id) links table 1 to tables 2, 3, and 4. And a foreign key (postal_code) links the brewery_address table to the brewery_zvhi table.
This way we can analyze the Zillow Home Value Index at the postal codes that have breweries located in them.
The data base can be used to help answer questions like:
