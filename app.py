from flask import Flask,request,jsonify
import json
from errorLogger import *
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def hello_world():
    if request.method == 'POST':
        print(json.loads(request.data))
        op_json = request_handler(json.loads(request.data))
        return jsonify(op_json)

    elif request.method == 'GET':
        return jsonify({"request":"GET request"})

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True, port=5000) #run app in debug mode on port 5000