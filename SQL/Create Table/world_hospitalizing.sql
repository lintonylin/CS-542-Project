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