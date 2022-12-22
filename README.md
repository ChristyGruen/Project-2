<h1> Project-2: Extract Transform Load </h1>
<h3>  </h3>

For this project we decided to investigate if breweries and home values have any correlation.

The brewery API data we used is from a free, open database containing brewery information from around the world. The data retrieved from the API call included information like a unique brewery id, brewery name, brewery type, address, city, state, postal code, country, longitude, latitude, phone number, and website url. According to the website we got the data from the dataset was last updated in October 2022.

https://www.openbrewerydb.org/documentation
<hr />

The home value data was retrieved from Zillow. Zillow publishes housing data on their website by organinzing it by Data Type and Geography. The dataset (CSV) we used contained the Zillow Home Value Index (ZHVI) that was smoothed and seasonally adjusted. The data from the Zillow CSV we ended up using contained the postal code, county, and ZHVI from 11/30/2022. The original CSV contained all of the ZHVI information by month beginning in January 2000 through November 2022. We decided to omit previous months' data since we only were interested in current trends. 

https://www.zillow.com/research/data/
<hr />

<h3>Data extraction:</h3>
<br>
The Open Brewery data was obtained by querying the api https://api.openbrewerydb.org.  Due to api limitations, the data was pulled in 50 record batches for a total of 164 api calls. The api data was stored in a list of dictonaries which was used to create a pandas DataFrame.
This raw data was saved to the Resources folder as "breweries_all_rawdata.csv".
<br></br>
The Zillow data was obtained by downloading a CSV file from https://www.zillow.com/research/data/ page under Zillow Home Value Index (ZHVI) section with the selections Data Type "ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted($)" and Geography "Zip Code". This CSV file was then read into a pandas dataframe.
<hr />
<h3>Data Transformation:</h3>
<br>
Transformation of the Open Brewery data consisted of the following:
<ol>
  <li> selected for breweries within the United States,
  <li> standardized the "postal_code" or "zipcode" to an integer of five digits by removing the dash, removing the four digit postal code extension and changing the data type from string to numeric,
  <li> renamed the street column to address,
  <li> created a subset table containing only the desired columns:  'id', 'name', 'brewery_type', 'street', 'city', 'state', 'zipcode', 'country','longitude', 'latitude', 'phone', and 'website_url',
  <li> saved the clean data to "breweries_us_cleandata.csv".
</ol>
<br>
Transformation of the Zillow ZHSI data consisted of the following:
<ol>
  <li> created a subset table going from 284 columns to 6 columns: 'RegionName','State','City','Metro','CountyName','11/30/2022',
  <li> renamed the 11/30/2022 column to ZHVI (or Zillow Home Value Index),
  <li> created a smaller subset table to to merge with the Open Brewery data.
</ol>
The Zillow ZHSI and Open Brewery DataFrames were merged on "postal_code" or "zipcode" using a left join to preserve Zillow data from zip codes without breweries. The merged data was saved as mergeall.csv.
<hr />
<h3>Data Loading (Mongo database):</h3>

The Zillow ZHSI & Open Brewery merged DataFrame was used to create a list of dictionaries containing all of the relevant data.

A Mongo database "Proj2_ETL" and collection "homebrew" were created.  The list of dictionaries was inserted into the homebrew collection.
![alt text](Resources/Project2%20ETL%20Mongodb%20Screenshot%202022-12-20%20191856.png)
<hr />

<h3>Data Loading (SQL database):</h3>
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

The ZHVI data csv contained information from many more postal codes than the brewery data allowing us to gather information about areas that have breweries and areas that do not have breweries.

![alt text](ResourcesPB/SQL%20ERD.pgerd.png)
<hr />

<h3>Questions</h3>
By combining Brewery data with Zillow Home Value Index data we could use this information to answer questions like:
<ol>
  <li>Is the number of breweries correlated with home value in the same zipcode, county, state?
  <li>Do home values differ in areas that contain breweries versus areas that do not have breweries?
  <li>What types of breweries are commonly located in areas with different home values?
</ol>

With additional information we could look into things like: 
<ol>
  <li>The number of breweries correlated with states that have legalized other recreational drugs?
  <li>The crime rates in areas with breweries and without breweries based on location at the city, county, and state level.
</ol>

Overall the data can be used to pinpoint specific areas and socioeconomic groups that would be more receptive to having breweries nearby. Operating breweries in areas with higher home values could lead to a more successful business model.

![alt text](ResourcesPB/SQL%20Query%201.png)

<br>

**Credit:**

- Chris Gruenhagen
- Paul Brichta

December 2022
