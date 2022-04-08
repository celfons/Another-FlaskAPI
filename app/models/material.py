import datetime

from app import db, ma

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False)
    description= db.Column(db.Text, nullable=False)
    price = db.Column(db.Float(), default=0, nullable=False)
    category = db.Column(db.String(20), default="curso", nullable=False)
    items = db.Column(db.String(255))
    payment_link = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    library = db.relationship('Library', backref='material_library', lazy=True)

    def __init__(self, title, description, price, category, items, payment_link):
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.payment_link = payment_link

class MaterialSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title', 'description', 'price', 'category', 'items', 'payment_link', 'created_on')


material_schema = MaterialSchema()
materials_schema = MaterialSchema(many=True)