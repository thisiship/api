from flask import jsonify, request, Blueprint
import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

users = [
    {
        'id': 0,
        'username': 'tonisbones',
        'email': 'test@test.com',
        'password': bcrypt.hashpw(u'tester'.encode('utf-8'), bcrypt.gensalt())
    }
]

def check_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)


@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify(message="Missing username parameter."), 400
    if not password:
        return jsonify(message="Missing password parameter."), 400

    if username != users[0]['username'] or not check_password(password.encode('utf-8'), users[0]['password']):
        return jsonify(message="Bad login credentials"), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
