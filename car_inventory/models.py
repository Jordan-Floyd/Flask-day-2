from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref
import uuid
import secrets


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)



class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))
    max_speed = db.Column(db.String(50))
    doors = db.Column(db.String(50))
    horsepower = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)



    def __init__(self, make, model, color, max_speed, doors, horsepower, user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.color = color
        self.max_speed = max_speed
        self.doors = doors
        self.horsepower = horsepower
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe)



class CarSchema(ma.Schema):
    class Meta:
        fields = ['id','make','model','color','max_speed','doors','horsepower']

car_schema = CarSchema()
cars_schema = CarSchema(many = True)