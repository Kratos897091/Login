from flask import Flask, jsonify, request
from pymongo import mongo_client

app = Flask(__name__)

@app.route("/signin",methods =['get'])
def sign():
    data = "hello"
    return jsonify({'data':data})

client = mongo_client("mongodb+srv://Jenn:Janki6121@cluster0.vqk5j27.mongodb.net/?retryWrites=true&w=majority")    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
