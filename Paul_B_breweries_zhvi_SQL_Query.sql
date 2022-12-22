-- Drop table if it exists
DROP TABLE brewery_id;
DROP TABLE brewery_address;
DROP TABLE brewery_location;
DROP TABLE brewery_contact;
DROP TABLE brewery_zhvi;

-- Create brewery_id table and view column datatypes
CREATE TABLE brewery_id (
	id VARCHAR primary key,
	name VARCHAR,
	brewery_type VARCHAR
);

-- Create brewery_address table and view column datatypes
CREATE TABLE brewery_address (
	id VARCHAR primary key references brewery_id (id),
	address VARCHAR,
	city VARCHAR,
	state VARCHAR,
	postal_code INT,
	country VARCHAR
);

-- Create brewery_location table and view column datatypes
CREATE TABLE brewery_location (
	id VARCHAR primary key references brewery_id (id),
	longitude VARCHAR,
	latitude VARCHAR
);

-- Create brewery_contact table and view column datatypes
CREATE TABLE brewery_contact (
	id VARCHAR primary key references brewery_id (id),
	phone VARCHAR,
	website_url VARCHAR
);

-- Create brewery_zhvi and view column datatypes
CREATE TABLE brewery_zhvi (
	postal_code INT primary key,
	county VARCHAR,
	ZHVI FLOAT	
);

-- Create a foreign key that links the Zillow Home Value Index data to the brewery_address table on postal_code
ALTER TABLE brewery_address
add constraint brewery_address_postal_code_fkey FOREIGN KEY (postal_code) references brewery_zhvi (postal_code);

SELECT * FROM brewery_id;
SELECT * FROM brewery_address;
SELECT * FROM brewery_location;
SELECT * FROM brewery_contact;
SELECT * FROM brewery_zhvi;