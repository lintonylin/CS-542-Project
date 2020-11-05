from flask import Flask,render_template,request
import pymysql

app = Flask(__name__)
conn = pymysql.connect(user='admin', host='cs542.chpy8wzjpky3.us-east-1.rds.amazonaws.com', passwd='Norwich123', db='innodb',cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('base.html')

type_number = 0

@app.route('/gets/',methods=['POST'])
def search():
    qtype = request.values.get('qt')
    if qtype == 'cases in a week':
        type_number = 1
        return render_template('search1.html')
    elif qtype == 'cases on a day':
        type_number = 2
        return render_template('search2.html')
    elif qtype == 'hospitalized rate':
        type_number = 3
        return render_template('base.html')
    elif qtype == 'new cases':
        type_number = 4
        return render_template('search4.html')
    elif qtype == 'new deaths':
        type_number = 5
        return render_template('search5.html')
@app.route('/1/',methods=['POST'])
def search1():
    Date1 = request.values.get('date1')
    Date2 = request.values.get('date2')
    County = request.values.get('county')
    sql = 'select cases as cases,date,county from innodb.US_COUNTY_TEST where county like' + County +' and date between '+Date1+' and '+Date2+';'
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('search1.html',items=datas)

@app.route('/2/',methods=['POST'])
def search2():
    Date = request.values.get('date')
    State = request.values.get('state')
    County = request.values.get('county')
    sql = "select * from innodb.UsCountyCaseInformation where state like '%" + State + "%' and dat = '" + Date + "' and us_county like '%" + County + "%'"
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('search2.html',items=datas)

@app.route('/4/',methods=['POST'])
def search4():
    if request.values.get('country') == '':
        startdate = "\"" + request.values.get('startdate') + "\""
        enddate = "\"" + request.values.get('enddate') + "\""
        query = "SELECT a.Country_Region, a.weekly_positive as positive, CONCAT( ROUND( a.weekly_positive / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {0} and dat < {1} group by Country_Region ) a,(Select sum(weekly_positive) As weekly_sum from (Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {2} and dat < {3} group by Country_Region) As temp) b order by a.weekly_positive desc; ".format(
            startdate, enddate, startdate, enddate)
        cur.execute(query)
        datas = cur.fetchall()
        result = []
        for data in datas:
            percent = float(data['percent'].replace('%', ''))
            if percent != 0:
                result.append(data)
        return render_template('search4.html', items=result)
    else:
        startdate = "\"" + request.values.get('startdate') + "\""
        enddate = "\"" + request.values.get('enddate') + "\""
        country = "\"" + request.values.get('country') + "\""
        query = "SELECT a.Country_Region, a.weekly_positive as positive, CONCAT( ROUND( a.weekly_positive / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {0} and dat < {1} group by Country_Region ) a,(Select sum(weekly_positive) As weekly_sum from (Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {2} and dat < {3} group by Country_Region) As temp) b where a.Country_Region={4}; ".format(startdate, enddate, startdate, enddate, country)
        cur.execute(query)
        datas = cur.fetchall()
        return render_template('search4.html',items=datas)


@app.route('/5/',methods=['POST'])
def search5():
    if request.values.get('country') == '':
        startdate = "\"" + request.values.get('startdate') + "\""
        enddate = "\"" + request.values.get('enddate') + "\""
        query = "SELECT a.Country_Region, a.weekly_death as death, CONCAT( ROUND( a.weekly_death / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM ( Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {0} and dat < {1} group by Country_Region) a,(Select sum(weekly_death) As weekly_sum from (Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {2} and dat < {3} group by Country_Region) AS temp) b order by a.weekly_death desc; ".format(
            startdate, enddate, startdate, enddate)
        cur.execute(query)
        datas = cur.fetchall()
        result = []
        for data in datas:
            percent = float(data['percent'].replace('%', ''))
            if percent != 0:
                result.append(data)
        return render_template('search5.html', items=result)
    else:
        startdate = "\"" + request.values.get('startdate') + "\""
        enddate = "\"" + request.values.get('enddate') + "\""
        country = "\"" + request.values.get('country') + "\""
        query = "SELECT a.Country_Region, a.weekly_death as death, CONCAT( ROUND( a.weekly_death / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM ( Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {0} and dat < {1} group by Country_Region) a,(Select sum(weekly_death) As weekly_sum from (Select Country_Region, sum(death) AS weekly_death from innodb.world_death Where dat > {2} and dat < {3} group by Country_Region) AS temp) b where a.Country_Region={4}; ".format(startdate, enddate, startdate, enddate, country)
        cur.execute(query)
        datas = cur.fetchall()
        return render_template('search5.html',items=datas)



if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port='8080')
