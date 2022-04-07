from app import db
from flask import request, jsonify
from ..models.library import Library, library_schema, libraries_schema

def post_library():
    pay_id = request.json['pay_id']
    status = request.json['status']
    user_id = request.json['user_id']
    material_id = request.json['material_id']

    library = Library(pay_id, status, user_id, material_id)

    try:
        db.session.add(library)
        db.session.commit()
        return jsonify({}), 204
    except :
        return jsonify({'message': 'unable to create', 'data': {}}), 500