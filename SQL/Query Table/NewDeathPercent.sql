Select Country_Region, sum(death) AS weekly_death
from innodb.world_death
Where dat >'2020-03-07' and dat < '2020-03-14' 
group by Country_Region;

Select sum(weekly_death) AS weekly_sum
from 
(Select Country_Region, sum(death) AS weekly_death
from innodb.world_death
Where dat >'2020-03-07' and dat < '2020-03-14' 
group by Country_Region)
AS temp;

SELECT
a.Country_Region,
CONCAT( ROUND( a.weekly_death / b.weekly_sum * 100, 2 ), '', '%' ) AS percent 
FROM
( Select Country_Region, sum(death) AS weekly_death
from innodb.world_death
Where dat >'2020-03-07' and dat < '2020-03-14' 
group by Country_Region) a,
(
Select sum(weekly_death) As weekly_sum
from (
Select Country_Region, sum(death) AS weekly_death
from innodb.world_death
Where dat >'2020-03-07' and dat < '2020-03-14' 
group by Country_Region
)
AS temp
) b;