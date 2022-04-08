from app import app, db
from flask import request, jsonify
from ..models.library import Library, library_schema, libraries_schema
from ..models.users import Users
import stripe

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
        payment_intent = event['data']['object']
       
        pay_id = payment_intent.id
        status = payment_intent.payment_status
        email = payment_intent.customer_details.email
        payment_link = payment_intent.payment_link

        user = Users.query.filter(Users.email == email).one()

        library = Library(pay_id, status, user.id, payment_link)

        try:
            db.session.add(library)
            db.session.commit()
        except :
            return jsonify({'message': 'unable to create', 'data': {}}), 500

    else:
        print('Unhandled event type {}'.format(event['type']))
    
    return jsonify(success=True)

def update_library(id):
    status = request.json['status']
    library = Library.query.filter(Library.pay_id == id).one()

    if not library:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    if library:
        try:
            library.status = status
            db.session.commit()
            return jsonify({}), 204
        except:
            return jsonify({'message': 'unable to update', 'data':{}}), 500
