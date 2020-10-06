create table innodb.WorldStateLocation( 
Country_Region varchar(50),
Province_State varchar(50),
PRIMARY KEY(Country_Region, Province_State));

insert into innodb.WorldStateLocation
select distinct Country_Region,Province_State FROM innodb.tested_worldwide;
