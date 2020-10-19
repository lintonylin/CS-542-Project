from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()

inputjson = "{\"startdate\": \"2020-03-07\", \"enddate\": \"2020-03-14\"}"

inputjson = json.loads(inputjson)

startdate = "\"" + inputjson['startdate'] + "\"" # input json
enddate = "\"" + inputjson['enddate'] + "\"" # input json

query = "SELECT a.Country_Region, a.weekly_positive, CONCAT( ROUND( a.weekly_positive / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {0} and dat < {1} group by Country_Region ) a,(Select sum(weekly_positive) As weekly_sum from (Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {2} and dat < {3} group by Country_Region) As temp) b; ".format(startdate, enddate, startdate, enddate)


c.execute(query)

result = c.fetchall()

# store result in json
outputjson = {}
for r in result:
    outputjson[r[0]] = []
    outputjson[r[0]].append(int(r[1]))
    outputjson[r[0]].append(r[2])

print(json.dumps(outputjson))
