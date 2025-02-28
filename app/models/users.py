import datetime
from app import db, ma

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    library = db.relationship('Library', backref='users_library', lazy=True)
    first_login = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, username, password, name, email, phone):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.phone = phone
        self.first_login = True

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'name', 'email', 'phone', 'password', 'created_on', 'first_login')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)