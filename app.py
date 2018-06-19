from flask import Flask,request,jsonify
import json
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def hello_world():
    if request.method == 'POST':
        print(json.loads(request.data))
        return jsonify(json.loads(request.data))

    elif request.method == 'GET':
        return jsonify({"request":"GET request"})

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000