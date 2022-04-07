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