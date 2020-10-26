import pymysql

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()
startdate = "\'2020-03-07\'"
enddate = "\'2020-03-14\'"
c.execute('Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat >' + startdate +'and dat <'+ enddate +'group by Country_Region;')

result = c.fetchall()
print(result)
