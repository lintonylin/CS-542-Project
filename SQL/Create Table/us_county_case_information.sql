create table innodb.UsCountyCaseInformation( 
cases varchar(50),
deaths integer,
Dat date,
Country_Region varchar(50),
State varchar(50),
Us_county varchar(50),
PRIMARY KEY pk_uscases (Dat, Country_Region, State, Us_county),
FOREIGN KEY fk_location (Country_Region, State, Us_county) REFERENCES innodb.UsCountyLocation(Country_Region, State, Us_county),
FOREIGN KEY fk_state (Country_Region, State) REFERENCES innodb.WorldStateLocation(Country_Region, Province_State)
);

insert into innodb.UsCountyCaseInformation
select cases, deaths, date, "United States" as Country_Region, state, county FROM innodb.US_COUNTY_TEST;
