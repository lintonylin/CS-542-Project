select * from innodb.tested_worldwide;
Create table innodb.world_hospitalizing (hospitalized integer,
recovered integer, 
dat date , 
hospitalizedcurr integer,
CountryRegion varchar (50) REFERENCES innodb.WorldStateLocation(Country_Region),
ProvinceState varchar (50) REFERENCES innodb.WorldStateLocation(Province_State),
PRIMARY KEY pk_uscases (dat,CountryRegion,ProvinceState)
);
replace into innodb.world_hospitalizing
select hospitalized, recovered, Date, hospitalizedCurr , Country_Region,  Province_State from innodb.tested_worldwide;

WorldTestingselect ifnull(sum(cases),0) as cases from innodb.US_COUNTY_TEST where county like "Cook" and date between '2020-01-21' and '2020-01-27';
select * from worldtesting;
select  cases as cases,date from innodb.US_COUNTY_TEST where county like "Orange" and date > '2020-01-21' and date <='2020-01-27';
select * from innodb.US_COUNTY_TEST where county like "Orange";
select * from innodb.US_COUNTY_TEST;