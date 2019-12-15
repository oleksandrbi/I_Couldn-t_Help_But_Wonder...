from flask import Flask
import pymysql

def getConnection():
    connection = pymysql.connect(host='10.22.12.131',
                                 user='root',
                                 password='SCL$Xdat4ML',
                                 db='Wonder',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def execute(con,sql,commit=False):
    print("Executing :", sql)
    with con:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        if(commit):
            con.commit()
        return rows

app = Flask(__name__)

@app.route("/")
def res():
    return "Testing"

@app.route("/res/<name>")
def display_res(name):
    return (name)

if __name__ == "__main__":
    app.run()
