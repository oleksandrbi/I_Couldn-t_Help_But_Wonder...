from flask import Flask
from sqlMethods import *
import pymysql
import json

# to install : pip3 install flask

app = Flask(__name__)

@app.route("/")
def res():
    return "Testing"

@app.route('/api/cdate', methods=['GET'])
def get_time():
    s = '{'
    for item in container.query_items(
                    query='SELECT tweets.date FROM tweets where tweets.date >= "2019-10-01" and tweets.date <= "2019-11-01"',
                    enable_cross_partition_query=True):
        jtime = item['date']
        head, text, end = jtime.partition('T')
        rtime = datetime.strptime(head, '%Y-%m-%d').timetuple()
        unixt = int(time.mktime(rtime))
        s = s + str(unixt) + ':' + str(1) + ','
    s = s[:-1]
    s = s + '}'
    return json.dumps(s)

@app.route("/listRes",methods = ['GET'])
def get_restaurants():
    con = getConnection()
    sql = "SELECT restaurant_id, restaurant_name FROM restaurant_data WHERE queries_set=1"
    data =  execute(con,sql)
    return json.dumps(data)

@app.route("/res/<name>",methods = ['GET'])
def display_res(name):
    return (name)

if __name__ == "__main__":
    app.run()
