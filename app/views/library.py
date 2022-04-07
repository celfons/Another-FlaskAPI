from app import app, db
from flask import request, jsonify
from ..models.library import Library, library_schema, libraries_schema
import stripe

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

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']

        pay_id = payment_intent.id
        status = payment_intent.status

        id = payment_intent.statement_descriptor.split(".")

        user_id = id[0]
        material_id = id[1]

        library = Library(pay_id, status, user_id, material_id)

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
