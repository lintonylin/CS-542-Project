select Dat, Country_Region, max(cast(death as decimal)) - min(cast(death as decimal)) as increment, max(cast(death as decimal)) as total from innodb.world_death
 where (dat = date_sub(cast('2020-09-16' as date), interval 1 day) or dat = '2020-09-16') and Country_Region like '%United States%' and Province_State='All States'
 group by Country_Region