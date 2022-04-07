from app import app
from flask import jsonify, url_for, redirect
from ..views import users, helper

@app.route('/', methods=['GET'])
def health():
    return jsonify({"System": "UP"})  

@app.route('/v1', methods=['GET'])
@helper.token_required
def root(current_user):
    response = []
    for result in current_user.library:
        response.append({
            "url" : result.material.url,
            "category" : result.material.category,
            "title" : result.material.title,
            "description" : result.material.description
        })
    return jsonify({'name': f'{current_user.name}', 'libraries' : response })


@app.route('/v1/authenticate', methods=['POST'])
def authenticate():
    return helper.auth()


@app.route('/v1/users', methods=['GET'])
@helper.token_required
def get_users():
    return users.get_users()


@app.route('/v1/users/<id>', methods=['GET'])
@helper.token_required
def get_user(id):
    return users.get_user(id)


@app.route('/v1/users', methods=['POST'])
@helper.token_required
def post_users():
    return users.post_user()


@app.route('/v1/users/<id>', methods=['DELETE'])
@helper.token_required
def delete_users(id):
    return users.delete_user(id)


@app.route('/v1/users/<id>', methods=['PUT'])
@helper.token_required
def update_users(id):
    return users.update_user(id)