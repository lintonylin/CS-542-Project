SELECT
a.Country_Region,
a.weekly_tested,
CONCAT( ROUND( a.weekly_tested / b.weekly_sum * 100, 2 ), '', '%' ) AS percent 
FROM
( Select Country_Region, sum(daily_tested) As weekly_tested
from innodb.WorldTesting
where dat > '2020-03-07' and dat < '2020-03-14' and Province_State='All States'
group by Country_Region ) a,
(
Select sum(weekly_tested) As weekly_sum
from (
	Select Country_Region, sum(daily_tested) As weekly_tested
	from innodb.WorldTesting
	where dat > '2020-03-07' and dat < '2020-03-14' and Province_State='All States'
	group by Country_Region
) As temp
) b
where a.Country_Region='United States'; 
