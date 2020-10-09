Select Country_Region, sum(daily_positive) As weekly_positive
from innodb.world_hospitalizing
where dat > '2020-03-01' and dat < '2020-03-31' 
and Country_Region = '';


Select sum(weekly_positive) As weekly_sum
from (
	Select Country_Region, sum(daily_positive) As weekly_positive
	from innodb.WorldTesting
	where dat > '2020-03-07' and dat < '2020-03-14' 
	group by Country_Region
) As temp;


SELECT
a.Country_Region,
a.weekly_positive,
CONCAT( ROUND( a.weekly_positive / b.weekly_sum * 100, 2 ), '', '%' ) AS percent 
FROM
( Select Country_Region, sum(daily_positive) As weekly_positive
from innodb.WorldTesting
where dat > '2020-03-07' and dat < '2020-03-14' 
group by Country_Region ) a,
(
Select sum(weekly_positive) As weekly_sum
from (
	Select Country_Region, sum(daily_positive) As weekly_positive
	from innodb.WorldTesting
	where dat > '2020-03-07' and dat < '2020-03-14' 
	group by Country_Region
) As temp
) b; 
