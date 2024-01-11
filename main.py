from database.db_manager import DbManager
from datetime import datetime
from time import sleep
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'twojTajnyKlucz'

users = {
    "user1": generate_password_hash("haslo123"),
    "user2": generate_password_hash("bezpiecznehaslo")
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['public_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if auth.username in users and check_password_hash(users[auth.username], auth.password):
        token = jwt.encode({'public_id': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/secure', methods=['GET'])
@token_required
def secure_route(current_user):
    return jsonify({'message': f'Hello, {current_user}. You are looking at a secure endpoint!'})

if __name__ == '__main__':
    app.run(debug=True)

