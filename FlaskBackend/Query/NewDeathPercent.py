# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:41:21 2020

@author: hawks
"""

#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
from datetime import datetime

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()

#Validate input
def validate(date_text):
    try:
         datetime.strptime(startdate, "%Y-%m-d")
    except ValueError:
          print("This is the incorrectdate format. It should be YYYY-MM-DD")

#Get user input
startdate = input("What is the startdate(format: yyyy-mm-dd): ")

validate(startdate)

enddate = input("What is the enddate(format: yyyy-mm-dd): ")

validate(enddate)

#Execute query
c.execute("SELECT a.Country_Region, CONCAT( ROUND( a.weekly_death / b.weekly_sum * 100, 2 ), '', '%' ) AS percent FROM( Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > '"+ startdate+"' and dat < '"+ enddate +"' group by Country_Region) a,(Select sum(weekly_death) As weekly_sum from (Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > '"+ startdate +"' and dat < '"+ enddate +"' group by Country_Region) AS temp) b;")

result = c.fetchall()

#Validate result 
if len(result) == 0:
    print("Please try it again with correct date format")
else: 
    print(result)

#Write json
Death_result = []

for i in range(len(result)):
    country = result[i][0]
    Death_result = Death_result + [[country, result[i][1]]]

with open ("NewDeathPercentbyCountry.json","w") as f:
    json.dump(Death_result, f)
   