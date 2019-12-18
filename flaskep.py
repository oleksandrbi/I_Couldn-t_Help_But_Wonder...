from flask import *
from flask_cors import CORS
from sqlMethods import *
import pymysql
import json

# to install : pip3 install flask
# pip3 install -U flask-cors

#for converting datetimes to json
def dtJson(dt):
    if isinstance(dt, datetime):
        return dt.__str__()



app = Flask(__name__)
CORS(app)

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
def listRes():
    con = getConnection()
    sql = "SELECT restaurant_id, restaurant_name FROM restaurant_data WHERE queries_set=1"
    data =  execute(con,sql)
    con.close()
    return json.dumps(data)

@app.route("/get_restaurant/<rest_id>",methods = ['GET'])
def get_restaurant(rest_id):
    con = getConnection()
    sql = "SELECT * from restaurant_data WHERE restaurant_id = '%s'" % rest_id
    data = execute(con,sql)
    con.close()
    if len(data) > 0:
        return json.dumps(data[0])
    else:
        #id not valid id
        abort(404)

#you can adjust this to get less data by changing * to the columns you need
@app.route("/get_tweets/<rest_id>",methods = ['GET'])
def get_tweets(rest_id):
    con = getConnection()
    sql = "SELECT * from raw_tweets WHERE restaurant_id = '%s' ORDER BY timestamp DESC LIMIT 20" % rest_id
    data = execute(con, sql)
    con.close()
    if len(data) > 0:
        return json.dumps(data,default = dtJson)
    else:
        #id not valid id
        abort(404)




if __name__ == "__main__":
    app.run()
