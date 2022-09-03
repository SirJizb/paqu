from flask import Flask, render_template
import json
import pymysql

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index1.html')


@app.route('/test', methods=['POST'])
def mytest():
    con = pymysql.connect(host='localhost', user='root', passwd='123456', db='db', port=3306, charset='utf8')
    cur = con.cursor()
    sql = 'select * from keywords'
    cur.execute(sql)
    see = cur.fetchall()
    keyword = []
    jsonData = {}
    for data in see:
        keyword.append(data[0])
    jsonData['keyword'] = keyword
    j = json.dumps(jsonData)

    cur.close()
    con.close()
    return j


if __name__ == '__main__':
    app.run(debug=True)
