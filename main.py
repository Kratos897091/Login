from flask import Flask, jsonify, request
from pymongo import MongoClient
import jwt

app = Flask(__name__)
client = MongoClient(
    "mongodb+srv://Jenn:Janki6121@cluster0.vqk5j27.mongodb.net")
db = client['userData']
collection = db['Data']


@app.route("/signup", methods=['POST'])
def sign():
    try:
        data = request.json
        name = data['name']
        username = data['username']
        password = data['password']
        email = data['email']

        user = {
            'name': name,
            'username': username,
            'password': password,
            'email': email
        }
        existing = collection.find_one({'email': email})
        existingusername = collection.find_one({'username': username})
        if existing:
            return jsonify({'email': email, 'message': "Already registered"})
        elif existingusername:
            return jsonify({'username': username, 'message': "Username not available"})
        else:
            collection.insert_one(user)
            return jsonify({'message': 'User created successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/signin", methods=['GET'])
def signin():
    try:
        data = request.json
        email = data['email']
        password = data['password']

        user = collection.find_one({'email': email})

        if user and user['password'] == password:
            token = jwt.encode({'email': email}, 'Gautam', algorithm='HS256')
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'User not found or incorrect password'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update', methods=['POST'])
def update():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        newpass = data['newpassword']

        user = collection.find_one({'email': email})

        if user and user['password'] == password:
            collection.update_one(
                {'email': email}, {'$set': {'password': newpass}})
            return jsonify({"message": "Password updated successfully"})
        else:
            return jsonify({"message": "User not found or incorrect password"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete', methods=['POST'])
def delete():
    try:
        data = request.json
        email = data['email']
        password = data['password']

        user = collection.find_one({'email': email})

        if user and user['password'] == password:
            collection.delete_one({'email': email})
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"message": "User not found or incorrect password"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
