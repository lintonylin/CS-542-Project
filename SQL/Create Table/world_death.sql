
Create table innodb.world_death( 
dat date, 
death integer,
Country_Region varchar(50),
Province_State varchar(50),
PRIMARY KEY pk_worldhealth (dat, Country_Region, Province_State),
FOREIGN KEY fk_Country(Country_Region, Province_State) REFERENCES innodb.WorldStateLocation(Country_Region, Province_State)
);


insert into innodb.world_death
Select distinct date, death, Country_Region, Province_State 
from innodb.tested_worldwide;



