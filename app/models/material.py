import datetime

from app import db, ma

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False)
    description= db.Column(db.Text, nullable=False)
    price = db.Column(db.Float(), default=0, nullable=False)
    category = db.Column(db.String(20), default="curso", nullable=False)
    url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    user = db.relationship('Users', back_populates='material')
    library = db.relationship('Library', backref='material_library', lazy=True)

    def __init__(self, title, description, price, category, url, user_id):
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.url = url
        self.user_id = user_id      

class MaterialSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title', 'description', 'price', 'category', 'url', 'user_id', 'created_on')


material_schema = MaterialSchema()
material_schema = MaterialSchema(many=True)