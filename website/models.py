from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))  # 减少到1000字符，练手够用
    date = db.Column(db.DateTime, default=func.now())  # 简化，去掉timezone
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
