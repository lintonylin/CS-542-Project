#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
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

#input startdate
startdate = "\"" + inputjson['startdate']+ "\""
enddate = "\"" +inputjson['enddate']+"\""

query = "SELECT a.Country_Region, a.weekly_death, CONCAT( ROUND( a.weekly_death / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM ( Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {0} and dat < {1} group by Country_Region) a,(Select sum(weekly_death) As weekly_sum from (Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {2} and dat < {3} group by Country_Region) AS temp) b order by a.weekly_death desc;".format(startdate, enddate, startdate, enddate)


c.execute(query)

result = c.fetchall()

queryouput = {}

for r in result:
    queryouput[r[0]] = []
    queryouput[r[0]].append(int(r[1]))
    queryouput[r[0]].append(r[2])
    
print(json.dumps(queryouput))
