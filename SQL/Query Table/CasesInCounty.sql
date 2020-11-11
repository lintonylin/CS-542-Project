
SELECT state, us_county, max(cast(cases as decimal)) - min(cast(cases as decimal)) as result FROM innodb.UsCountyCaseInformation
where state='Massachusetts' and (dat=date_sub(cast('2020-03-11' as date),interval 1 day) or dat='2020-03-11')
group by state, us_county;
