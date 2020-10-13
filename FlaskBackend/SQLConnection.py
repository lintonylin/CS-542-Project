from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()

c.execute('Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > \'2020-03-07\' and dat < \'2020-03-14\' group by Country_Region;')

result = c.fetchall()
print(result)
