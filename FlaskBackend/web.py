from flask import Flask,render_template,request
import pymysql
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('base.html')
if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port='8080')