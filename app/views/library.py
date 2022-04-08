from app import app, db
from flask import request, jsonify
from ..models.library import Library, library_schema, libraries_schema
from ..models.users import Users
from ..models.material import Material
import stripe
import random
import string
from werkzeug.security import generate_password_hash

def get_all(current_user):
    response = []
    for result in current_user.library:
        print(result.material.url)
        if(result.status == 'paid'):
            response.append({
                "url" : result.material.url,
                "category" : result.material.category,
                "title" : result.material.title,
                "description" : result.material.description
            })
    return jsonify({'name': f'{current_user.name}', 'libraries' : response })

def post_library():

    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, app.config['STRIPE_SECRET']
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    if event['type'] == 'checkout.session.completed':
        payment = event['data']['object']
       
        pay_id = payment.payment_intent
        status = payment.payment_status
        email = payment.customer_details.email
        name = payment.customer_details.name
        phone = payment.customer_details.phone
        payment_link = payment.payment_link
       
        try:
            material = Material.query.filter(Material.payment_link == payment_link).one()
            user = Users.query.filter(Users.email == email).first()
            if not user:
                gen = string.ascii_letters + string.digits + string.ascii_uppercase
                password = ''.join(random.choice(gen) for i in range(12))
                pass_hash = generate_password_hash(password)
                user = Users(email, pass_hash, name, email, phone)
                db.session.add(user)
                db.session.commit()
            library = Library(pay_id, status, user.id, material.id)
       
            db.session.add(library)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to create', 'data': {}}), 500
    if event['type'] == 'charge.refunded':
        refunded = event['data']['object']
        pay_id = refunded.payment_intent
        
        try:
            library = Library.query.filter(Library.pay_id == pay_id).one()
            if library:
                library.status = "refunded"
                db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to create', 'data': {}}), 500
    else:
        print('Unhandled event type {}'.format(event['type']))
    
    return jsonify(success=True)

def update_library(id):
    status = request.json['status']
    library = Library.query.filter(Library.pay_id == id).first()

    if not library:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    if library:
        try:
            library.status = status
            db.session.commit()
            return jsonify({}), 204
        except:
            return jsonify({'message': 'unable to update', 'data':{}}), 500
