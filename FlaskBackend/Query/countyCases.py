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

# read from input json file
with open("countyCaseInput.json", "r") as f:
	queryInput = json.load(f)
	dat = queryInput["dat"]
	state = queryInput["state"]
	us_county = queryInput["us_county"]

state_result = dict()
county_result = dict()

if len(us_county):		# if county is specified, return result of that county
	c.execute("Select cases from innodb.UsCountyCaseInformation where dat = '" + dat + "' and state = '" + state + "' and us_county = '" + us_county + "';")
	result = c.fetchall()
	county_result[us_county] = result[0][0]
else:		# if not, then return result of the state
	c.execute("Select us_county, cases from innodb.UsCountyCaseInformation where dat = '" + dat + "' and state = '" + state + "';")
	result = c.fetchall()
	for i in range(len(result)):
		county = result[i][0]
		county_result[county] = result[i][1]

# output to json file
state_result[state + " " + dat] = county_result
with open(state + " " + us_county + " " + dat + ".json", "w") as f:
	json.dump(state_result, f)
	print("Result is written to JSON file " + state + " " + us_county + " " + dat + ".json")
