select Country, countryRec as Recovered, countryHos as Hospitalized, countryCase as Total_Cases, countryRec/countryCase as Recover_Rate, countryHos/countryCase as Hospitalized_Rate
from (
select max(recSum) - min(recSum) as countryRec 
from 
(select  dat, sum(recovered) as recSum from innodb.world_hospitalizing 
where CountryRegion = 'United States' and (dat = '2020-05-01' or dat = '2020-06-01')
group by dat) as t3) as t4, (select max(caseSum)-min(caseSum) as countryCase from 
(select dat, sum(cases) as caseSum from innodb.WorldTesting
where Country_Region = 'United States' and (dat = '2020-05-01' or dat='2020-06-01')
group by dat) as t1) as t5,
(select distinct CountryRegion as Country from innodb.world_hospitalizing 
where CountryRegion = 'United States')as t6,
(
select max(HosSum) - min(HosSum) as countryHos
from 
(select  dat, sum(hospitalized) as HosSum from innodb.world_hospitalizing 
where CountryRegion = 'United States' and (dat = '2020-05-01' or dat = '2020-06-01')
group by dat) as t7) as t8;