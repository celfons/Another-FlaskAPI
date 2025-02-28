from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema


def get_users():
    name = request.args.get('name')
    if name:
        users = Users.query.filter(Users.name.like(f'%{name}%')).all()
    else:
        users = Users.query.all()
    if users:
        result = users_schema.dump(users)
        return jsonify({'message': 'successfully fetched', 'data': result})

    return jsonify({'message': 'nothing found', 'data': {}})


def get_user(id):
    user = Users.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully fetched', 'data': result}), 201

    return jsonify({'message': "user don't exist", 'data': {}}), 404


def post_user():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    user = user_by_username(username)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'user already exists', 'data': {}})

    pass_hash = generate_password_hash(password)
    user = Users(username, pass_hash, name, email, phone)

    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully registered', 'data': result.data}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500


def update_password(id):
    password = request.json['password']
    user = Users.query.get(id)

    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    pass_hash = generate_password_hash(password)

    if user:
        try:
            user.password = pass_hash
            user.first_login = False
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully updated', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to update', 'data':{}}), 500

def update_user(id):
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    user = Users.query.get(id)

    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    pass_hash = generate_password_hash(password)

    if user:
        try:
            user.username = username
            user.password = pass_hash
            user.name = name
            user.email = email
            phone.email = phone
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully updated', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to update', 'data':{}}), 500

def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully deleted', 'data': result.data}), 200
        except:
            return jsonify({'message': 'unable to delete', 'data': {}}), 500


def user_by_username(username):
    try:
        return Users.query.filter(Users.username == username).one()
    except:
        return None
