create table innodb.WorldTesting ( 
dat date, 
active integer, 
cases integer,
daily_positive integer,
daily_tested integer,
total_tested integer,
Country_Region varchar(50),
Province_State varchar(50),
PRIMARY KEY(dat, Country_Region, Province_State),
CONSTRAINT WT_fk
    FOREIGN KEY (Country_Region, Province_State) 
        REFERENCES innodb.WorldStateLocation(Country_Region, Province_State)
);

replace into innodb.WorldTesting
select Date, active, positive, daily_positive, daily_tested, total_tested, Country_Region, Province_State from innodb.WORLDWIDE_TEST;
