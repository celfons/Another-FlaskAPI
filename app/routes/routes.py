from app import app
from flask import jsonify, url_for, redirect
from ..views import users, helper, material, library

@app.route('/', methods=['GET'])
def health():
    return jsonify({"System": "UP"})  

@app.route('/v1/authenticate', methods=['POST'])
def authenticate():
    return helper.auth()

@app.route('/v1/users', methods=['GET'])
@helper.admin_required
def get_users():
    return users.get_users()

@app.route('/v1/users/<id>', methods=['GET'])
@helper.admin_required
def get_user(id):
    return users.get_user(id)

@app.route('/v1/users', methods=['POST'])
@helper.admin_required
def post_users():
    return users.post_user()

@app.route('/v1/users/<id>', methods=['DELETE'])
@helper.admin_required
def delete_users(id):
    return users.delete_user(id)

@app.route('/v1/users/<id>', methods=['PUT'])
@helper.admin_required
def update_users(id):
    return users.update_user(id)

@app.route('/v1/material/free', methods=['GET'])
def get_free_material():
    return material.get_free()

@app.route('/v1/material/premium', methods=['GET'])
def get_premium_material():
    return material.get_premium()

@app.route('/v1/material/category/<category>', methods=['GET'])
def get_category_material(category):
    return material.get_category(category)

@app.route('/v1/libraries', methods=['GET'])
@helper.user_required
def root(current_user):
    response = []
    for result in current_user.library:
        if(result.status == 'succeeded'):
            response.append({
                "url" : result.material.url,
                "category" : result.material.category,
                "title" : result.material.title,
                "description" : result.material.description
            })
    return jsonify({'name': f'{current_user.name}', 'libraries' : response })

@app.route('/v1/library', methods=['POST'])
@helper.admin_required
def post_library():
    return library.post_library()

@app.route('/v1/library/<id>', methods=['PUT'])
@helper.admin_required
def update_library(id):
    return library.update_library()

@app.route('/v1/material', methods=['POST'])
@helper.admin_required
def post_material():
    return material.post_material()

@app.route('/v1/material/<id>', methods=['PUT'])
@helper.admin_required
def update_material(id):
    return material.update_material(id)