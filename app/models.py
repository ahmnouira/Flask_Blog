
from app import db, App
from datetime import datetime
from werkzeug.security import  generate_password_hash  # to generate a hashed password
from werkzeug.security import check_password_hash      # to check the hashed password
from flask_login import UserMixin                      # includes generic implementations fro most User classes
from app import login                                  # import login
from hashlib import md5
from time import time                                   # import time
import jwt                                             # import JSON Web Token


class Role(db.Model):
    __tablename__ = 'ROLES_'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')  # one role can be assigned to many users

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))  # holds a hash of the user password
    role_id = db.Column(db.Integer, db.ForeignKey('ROLES_.id'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))   # about me
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):    # hashing method
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # validation password method
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # generate a jwt token string
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},   # jwt.encode return token as bytes
                          App.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        # .decode('utf-8') to retrun a string

    @staticmethod    # decorator for static method
    def verify_reset_password(token):   # static method do not receive the class as first arg (self)
        try:
            id_ = jwt.decode(token, App.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']

        except:

            return

        return User.query.get(id_)


class Post(db.Model):
    __tablename__ = "POSTS"                # the table name
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))

    def __repr__(self):
        return '<Post :{}>'.format(self.body)


@login.user_loader     # register
def load_user(id_):    # load the user id function
    return User.query.get(int(id_))

