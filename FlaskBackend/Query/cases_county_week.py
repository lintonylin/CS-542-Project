import pymysql

host = 'cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com'
user = 'admin'
password='Norwich123'
port=3306
conn = pymysql.connect(host, user=user, port=port, passwd=password)
c = conn.cursor()
Date1 = " \'2020-1-21\' "
Date2 = " \'2020-1-27\' "
County =" \'Orange\' "
c.execute('select cases as cases,date,county from innodb.US_COUNTY_TEST where county like' + County +' and date between '+Date1+' and '+Date2+';')

result = c.fetchall()
print(result)
