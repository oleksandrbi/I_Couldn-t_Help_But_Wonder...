from flask import *
from flask_cors import CORS
from sqlMethods import *
import pymysql
import json
import pandas as pd
import sys

# to install : pip3 install flask
# pip3 install -U flask-cors

#for converting datetimes to json
def dtJson(dt):
    if isinstance(dt, datetime):
        return dt.__str__()



app = Flask(__name__)
CORS(app)

@app.route("/get_id/<rest_name>")
def getIDFromName(rest_name):
    con = getConnection()
    sql = "SELECT restaurant_id from restaurant_data where restaurant_name='%s'" %rest_name
    resp = execute(con,sql)
    return resp[0]['restaurant_id'] 


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

@app.route("/get_sentiment/<rest_id>",methods = ['GET'])
def get_sentiment_count(rest_id):
    con = getConnection()
    sql ="""
    SELECT
    raw_tweets.tweet_id, raw_tweets.timestamp, calced_tweet_sentiments.sentiment
FROM
    raw_tweets
        JOIN
    calced_tweet_sentiments ON raw_tweets.tweet_id = calced_tweet_sentiments.tweet_id
WHERE
    raw_tweets.restaurant_id = '%s'
    """ % rest_id
    data = execute(con,sql)
    df = pd.DataFrame(data)
    df['date'] = df['timestamp'].dt.date
    df11=df[df['sentiment']==0].groupby(['date']).count()
    results = []
    length = len(df11.index)
    for x in range(7):
        results.append(int(df11['sentiment'][length-x-1]))
    results.reverse()
    print(results)
    sys.stdout.flush()
    return json.dumps(results, default = dtJson)





if __name__ == "__main__":
    app.run()
