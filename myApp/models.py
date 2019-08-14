from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    hashed = db.Column(db.String(150))
    password = db.Column(db.String(50))
    salt = db.Column(db.String(150))
    twits = db.relationship('Twits',backref='user', lazy=True)
    email = db.Column(db.String(150))

    def get_id(self):
        return self.user_id
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False

class Twits(db.Model):
   
    twit_id = db.Column(db.Integer, primary_key = True)
    twit = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
          return self.twit

class Images(db.Model):
    image_id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(150))
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    username = db.Column(db.String(50))
    description = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
          return self.image
