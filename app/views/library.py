from app import app, db
from flask import request, jsonify
from ..models.library import Library, library_schema, libraries_schema
from ..models.users import Users
from ..models.material import Material
import stripe
import random
import string
from werkzeug.security import generate_password_hash
import smtplib
import email.message
import json

def get_all(current_user):
    response = []
    for result in current_user.library:
        if(result.status == 'paid'):
            response.append({
                "id": result.material.id,
                "items" : json.loads(result.material.items),
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
        savePayment(payment)

    if event['type'] == 'charge.refunded':
        refunded = event['data']['object']
        saveRefunded(refunded.payment_intent)
    
    return jsonify(success=True)

def saveRefunded(pay_id):
    try:
        library = Library.query.filter(Library.pay_id == pay_id).one()
        if library:
            library.status = "refunded"
            db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'unable to create', 'data': {}}), 500

def savePayment(payment):
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
            db.session.flush()
            db.session.refresh(user)
            send_email(email, password)

        library = Library(pay_id, status, user.id, material.id)
    
        db.session.add(library)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'unable to create', 'data': {}}), 500


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

def send_email(email, password):
    corpo_email = "Sua senha para acessar a plataforma é: " + password

    msg = email.message.Message()
    msg['Subject'] = 'Senha da plataforma'
    msg['From'] = app.config['EMAIL_USERNAME']
    msg['To'] = email
    password = app.config['EMAIL_PASSWORD']
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    try:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    except Exception as e:
        print(e)
