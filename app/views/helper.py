import datetime
from functools import wraps
from app import app
from flask import request, jsonify
from .users import user_by_username
import jwt
from werkzeug.security import check_password_hash

def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': []}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_by_username(username=data['username'])
        except:
            return jsonify({'message': 'token is invalid or expired', 'data': []}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': []}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_by_username(username=data['username'])
            if current_user.username != app.config['ADMIN']:
                raise
        except:
            return jsonify({'message': 'only admin', 'data': []}), 401
        return f(*args, **kwargs)
    return decorated

def auth():
    username = request.json['username']
    password = request.json['password']
    if not username or not password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
    user = user_by_username(username)
    if not user:
        return jsonify({'message': 'user not found', 'data': []}), 401

    if user and check_password_hash(user.password, password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) },
                           app.config['SECRET_KEY'])
        return jsonify({'message': 'Validated successfully', 'token': token.decode('UTF-8'),
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=12), 'first_login' : user.first_login})

    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
