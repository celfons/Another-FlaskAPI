import datetime

from app import db, ma


class Library(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pay_id = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    material = db.relationship('Material', back_populates='library')
    custom_fields = db.Column(db.Text())

    def __init__(self, pay_id, status, user_id, material_id, custom_fields):
        self.pay_id = pay_id
        self.status = status
        self.user_id = user_id
        self.material_id = material_id
        self.custom_fields = custom_fields

class LibrarySchema(ma.Schema):

    class Meta:
        fields = ('id', 'pay_id', 'status', 'user_id', 'material_id', 'created_on', 'custom_fields')


library_schema = LibrarySchema()
libraries_schema = LibrarySchema(many=True)
