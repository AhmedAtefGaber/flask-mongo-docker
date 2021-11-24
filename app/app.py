from flask import Flask, request
import datetime, pymongo

app = Flask(__name__)

timeStamp = datetime.datetime.now().timestamp()
myclient = pymongo.MongoClient("mongodb://mongo:jPG1KhkyMP@db-svc:27017/")
dblist = myclient.list_database_names()

if "mydatabase" not in dblist:
    mydb = myclient["mydatabase"]
    mycol = mydb["strings"]

@app.route('/')
def query_string():
    
    str1 = request.args.get('str1')
    str2 = request.args.get('str2')
    fullStr = str1 + str2

    strings_collection = { 'str1' : str1, 'fullStr' : fullStr, 'timeStamp' : timeStamp }
    x = mycol.insert_one(strings_collection)

    return '''
              <h1>The str1 value is: {}</h1>
              <h1>The str2 value is: {}</h1>
              <h1>the full string is: {}</h1>'''.format(str1, str2, fullStr)