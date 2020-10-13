from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import pymysql
import json

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()

dat = '2020-06-02'
state = 'California'
us_county = 'Orange'

state_result = dict()

if len(us_county):		# if county is specified, return result of that county
	c.execute("Select cases from innodb.UsCountyCaseInformation where dat = '" + dat + "' and state = '" + state + "' and us_county = '" + us_county + "';")
	result = c.fetchall()
	county_result = [[us_county, result[0][0]]]
else:		# if not, then return result of the state
	c.execute("Select us_county, cases from innodb.UsCountyCaseInformation where dat = '" + dat + "' and state = '" + state + "';")
	result = c.fetchall()
	county_result = []
	for i in range(len(result)):
		county = result[i][0]
		county_result = county_result + [[county, result[i][1]]]

state_result[state] = county_result
with open(state + " " + us_county + " " + dat + ".json", "w") as f:
	json.dump(state_result, f)
	print("Result is written to JSON file")
