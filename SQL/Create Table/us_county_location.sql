create table innodb.UsCountyLocation ( 
Country_Region varchar(50),
State varchar(50),
Us_county varchar(50),
PRIMARY KEY(Country_Region, State, Us_county));

insert into innodb.UsCountyLocation
select distinct "United States" as Country_Region,state,county from innodb.US_COUNTY_TEST;
