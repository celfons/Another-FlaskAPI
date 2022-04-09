from app import app
from flask import jsonify, url_for, redirect
from ..views import users, helper, material, library
from flask_cors import CORS, cross_origin

@app.route('/', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
def health():
    return jsonify({"System": "UP"})  

@app.route('/v1/authenticate', methods=['POST'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
def authenticate():
    return helper.auth()

@app.route('/v1/users', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def get_users():
    return users.get_users()

@app.route('/v1/users/<id>', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def get_user(id):
    return users.get_user(id)

@app.route('/v1/users', methods=['POST'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def post_users():
    return users.post_user()

@app.route('/v1/users/<id>', methods=['DELETE'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def delete_users(id):
    return users.delete_user(id)

@app.route('/v1/users/<id>', methods=['PUT'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def update_users(id):
    return users.update_user(id)

@app.route('/v1/users/<id>/password', methods=['PUT'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def update_users(id):
    return users.update_password(id)

@app.route('/v1/material/free', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
def get_free_material():
    return material.get_free()

@app.route('/v1/material/premium', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
def get_premium_material():
    return material.get_premium()

@app.route('/v1/material/category/<category>', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
def get_category_material(category):
    return material.get_category(category)

@app.route('/v1/libraries', methods=['GET'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.user_required
def get_libraries(current_user):
    return library.get_all(current_user)

@app.route('/v1/library', methods=['POST'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
def post_library():
    return library.post_library()

@app.route('/v1/library/<id>', methods=['PUT'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def update_library(id):
    return library.update_library(id)

@app.route('/v1/material', methods=['POST'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def post_material():
    return material.post_material()

@app.route('/v1/material/<id>', methods=['PUT'])
@cross_origin(origin='http://celfons-api.herokuapp.com')
@helper.admin_required
def update_material(id):
    return material.update_material(id)