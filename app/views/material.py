from app import db
from flask import request, jsonify
from ..models.material import Material, material_schema, materials_schema

def get_free():
    materiais = Material.query.filter_by(price=0).all()
    response = []
    for material in materiais:
        response.append({
            "price" : material.price,
            "category" : material.category,
            "title" : material.title,
            "description" : material.description
        })
    return jsonify(response), 200

def get_premium():
    materiais = Material.query.filter(Material.price > 0).all()
    response = []
    for material in materiais:
        response.append({
            "price" : material.price,
            "category" : material.category,
            "title" : material.title,
            "description" : material.description
        })
    return jsonify(response), 200

def get_category(category):
    materiais = Material.query.filter_by(category=category).all()
    response = []
    for material in materiais:
        response.append({
            "price" : material.price,
            "category" : material.category,
            "title" : material.title,
            "description" : material.description
        })
    return jsonify(response), 200

def post_material():
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']
    category = request.json['category']
    url = request.json['url']

    material = material_by_title(title)
    if material:
        result = material_schema.dump(material)
        return jsonify({'message': 'user already exists', 'data': {}})

    material = Material(title, description, price, category, url)

    try:
        db.session.add(material)
        db.session.commit()
        result = user_schema.dump(material)
        return jsonify({'message': 'successfully registered', 'data': result.data}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500

def update_material(id):
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']
    category = request.json['category']
    url = request.json['url']
    material = Material.query.get(id)

    if not material:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    if material:
        try:
            material.title = title
            material.description = description
            material.price = price
            material.category = category
            material.url = url
            db.session.commit()
            result = user_schema.dump(material)
            return jsonify({'message': 'successfully updated', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to update', 'data':{}}), 500


def material_by_title(title):
    try:
        return Material.query.filter(Material.title == title).one()
    except:
        return None