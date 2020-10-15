#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
import pymysql

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()

startdate = '\'2020-03-07\'' # input json
enddate = '\'2020-03-14\'' # input json

query = "SELECT a.Country_Region, CONCAT( ROUND( a.weekly_death / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM ( Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {0} and dat < {1} group by Country_Region) a,(Select sum(weekly_death) As weekly_sum from (Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {2} and dat < {3} group by Country_Region) AS temp) b;".format(startdate, enddate, startdate, enddate)


c.execute(query)

result = c.fetchall()
print(result)
