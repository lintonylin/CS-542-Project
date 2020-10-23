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
        return render_template('base.html')
    elif qtype == 'cases on a day':
        type_number = 2
        return render_template('search2.html')
    elif qtype == 'hospitalized rate':
        type_number = 3
        return render_template('base.html')
    elif qtype == 'new cases':
        type_number = 4
        return render_template('base.html')
    elif qtype == 'new deaths':
        type_number = 5
        return render_template('base.html')

@app.route('/2/',methods=['POST'])
def search2():
    Date = request.values.get('date')
    State = request.values.get('state')
    County = request.values.get('county')
    sql = "select * from innodb.UsCountyCaseInformation where state like '%" + State + "%' and dat = '" + Date + "' and us_county like '%" + County + "%'"
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('search2.html',items=datas)


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port='8080')
