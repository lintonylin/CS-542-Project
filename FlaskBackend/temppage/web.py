import pymysql
from flask import Flask, render_template, request
import json
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
        return render_template('search3.html')
    elif qtype == 'new cases':
        type_number = 4
        return render_template('search4.html')
    elif qtype == 'new deaths':
        type_number = 5
        return render_template('search5.html')
    elif qtype == 'deaths on a day':
        type_number = 6
        return render_template('search6.html')


@app.route('/1/',methods=['POST'])
def search1():
    Date1 = request.values.get('date1')
    Date2 = request.values.get('date2')
    County = request.values.get('county')
    State = request.values.get ('state')
    sql = "select cases,date from innodb.US_COUNTY_TEST where county like '%" + County + "%' and state like '%" + State + "%'and date between '"+Date1+"' and '"+Date2+"';"
    cur.execute(sql)
    datas = cur.fetchall()
    print(datas)
    result = []

        # [{"cases": 1, 'date': '2020-1-25'}, {'cases': 1, 'date': '2020-1-26'}, {'cases': 1, 'date': datetime.datetime(2020, 1, 27, 0, 0)}]
    for data in datas:
        data['date'] = data['date'].strftime('%m-%d')
        result.append(data)
    r1=json.dumps(result, indent=4, sort_keys=True, default=str)
    print(r1)
    return render_template('search1.html',items=datas)

@app.route('/2/',methods=['POST'])
def search2():
    Date = request.values.get('date')
    State = request.values.get('state')
    County = request.values.get('county')
    sql = "select '"+Date+"' as Dat, State, Us_county, max(cast(cases as decimal)) - min(cast(cases as decimal)) as increment, max(cast(cases as decimal)) as total from innodb.UsCountyCaseInformation where state like '%" + State + "%' and (dat = date_sub(cast('" + Date + "' as date), interval 1 day) or dat = '" + Date + "') and us_county like '%" + County + "%' group by State, Us_county"
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('search2.html',items=datas)

@app.route('/3/',methods=['POST'])
def search3():
    Startdate = request.values.get('startdate')
    Enddate = request.values.get('enddate')
    Country = request.values.get('country')
    sql = "select Country, countryRec as Recovered, countryHos as Hospitalized, countryRec+countryHos+countryCase as Total_Cases, ROUND(countryCase/countryCase*100,2) as Total_rate ,ROUND(countryRec/(countryRec+countryHos+countryCase)*100, 2) as Recover_Rate, ROUND(countryHos/(countryRec+countryHos+countryCase)*100, 2) as Hospitalized_Rate from (select max(recSum) - min(recSum) as countryRec from (select  dat, sum(recovered) as recSum from innodb.world_hospitalizing where CountryRegion = '" +Country + "' and (dat = '" +Startdate+"' or dat = '"+Enddate+"') group by dat) as t3) as t4, (select max(caseSum)-min(caseSum) as countryCase from (select dat, sum(cases) as caseSum from innodb.WorldTesting where Country_Region = '" +Country + "' and (dat = '" +Startdate+"' or dat = '"+Enddate+"') group by dat) as t1) as t5, (select distinct CountryRegion as Country from innodb.world_hospitalizing where CountryRegion = '" +Country + "')as t6,(select max(HosSum) - min(HosSum) as countryHos from (select  dat, sum(hospitalized) as HosSum from innodb.world_hospitalizing where CountryRegion = '" +Country + "' and (dat = '" +Startdate+"' or dat = '"+Enddate+"') group by dat) as t7) as t8"
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('search3.html',items=datas)

@app.route('/4/',methods=['POST'])
def search4():
    if request.values.get('country') == '':
        startdate = "\"" + request.values.get('startdate') + "\""
        enddate = "\"" + request.values.get('enddate') + "\""
        query = "SELECT a.Country_Region, a.weekly_positive as positive, CONCAT( ROUND( a.weekly_positive / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {0} and dat < {1} and Province_State='All States' group by Country_Region ) a,(Select sum(weekly_positive) As weekly_sum from (Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {2} and dat < {3} and Province_State='All States' group by Country_Region) As temp) b order by a.weekly_positive desc; ".format(
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
        query = "SELECT a.Country_Region, a.weekly_positive as positive, CONCAT( ROUND( a.weekly_positive / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {0} and dat < {1} and Province_State='All States' group by Country_Region ) a,(Select sum(weekly_positive) As weekly_sum from (Select Country_Region, sum(daily_positive) As weekly_positive from innodb.WorldTesting where dat > {2} and dat < {3} and Province_State='All States' group by Country_Region) As temp) b where a.Country_Region={4}; ".format(startdate, enddate, startdate, enddate, country)
        cur.execute(query)
        datas = cur.fetchall()
        return render_template('search4.html',items=datas)


@app.route('/5/',methods=['POST'])
def search5():
    if request.values.get('country') == '':
        startdate = "\"" + request.values.get('startdate') + "\""
        enddate = "\"" + request.values.get('enddate') + "\""
        query = "SELECT a.Country_Region, a.weekly_tested as tested, CONCAT( ROUND( a.weekly_tested / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_tested) As weekly_tested from innodb.WorldTesting where dat > {0} and dat < {1} and Province_State='All States' group by Country_Region ) a,(Select sum(weekly_tested) As weekly_sum from (Select Country_Region, sum(daily_tested) As weekly_tested from innodb.WorldTesting where dat > {2} and dat < {3} and Province_State='All States' group by Country_Region) As temp) b order by a.weekly_tested desc; ".format(
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
        query = "SELECT a.Country_Region, a.weekly_tested as tested, CONCAT( ROUND( a.weekly_tested / b.weekly_sum * 100, 2 ), \'\', \'%\' ) AS percent FROM( Select Country_Region, sum(daily_tested) As weekly_tested from innodb.WorldTesting where dat > {0} and dat < {1} and Province_State='All States' group by Country_Region ) a,(Select sum(weekly_tested) As weekly_sum from (Select Country_Region, sum(daily_tested) As weekly_tested from innodb.WorldTesting where dat > {2} and dat < {3} and Province_State='All States' group by Country_Region) As temp) b where a.Country_Region={4}; ".format(startdate, enddate, startdate, enddate, country)
        cur.execute(query)
        datas = cur.fetchall()
        return render_template('search5.html',items=datas)

@app.route('/6/',methods=['POST'])
def search6():
    Date = request.values.get('date')
    Country = request.values.get('country')
    if len(Country) > 0:
        sql = "select Country_Region, increment, total from (select Country_Region, max(cast(death as decimal)) - min(cast(death as decimal)) as increment, max(cast(death as decimal)) as total from innodb.world_death where (dat = date_sub(cast('"+ Date + "' as date), interval 1 day) or dat = '" + Date + "') and Country_Region like '" + Country + "' and Province_State='All States'group by Country_Region) a where a.total != 0 order by total desc"
    else:
        sql = "select Country_Region, increment, total from (select Country_Region, max(cast(death as decimal)) - min(cast(death as decimal)) as increment, max(cast(death as decimal)) as total from innodb.world_death where (dat = date_sub(cast('" + Date + "' as date), interval 1 day) or dat = '" + Date + "') and Province_State='All States'group by Country_Region) a where a.total != 0 order by total desc"
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('search6.html',items=datas)


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port='8080')
