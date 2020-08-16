from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime
import hashlib
import os

db = SQLAlchemy()

association_table = db.Table('association', db.Model.metadata,
                             db.Column('product_id', db.Integer,
                                       db.ForeignKey('product.id')),
                             db.Column('category_id', db.Integer,
                                       db.ForeignKey('category.id'))
                             )


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    condition = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sold = db.Column(db.Boolean, nullable=False)
    image = db.Column(db.String)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    categories = db.relationship(
        'Category', secondary=association_table, back_populates='products')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.condition = kwargs.get('condition', '')
        self.price = kwargs.get('price')
        self.sold = kwargs.get('sold')
        self.image = kwargs.get('image')
        self.seller_id = kwargs.get('seller_id')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'condition': self.condition,
            'price': self.price,
            'sold': self.sold,
            'image': self.image,
            'seller_id': self.seller_id,
            'buyer_id': self.buyer_id
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    products = db.relationship(
        'Product', secondary=association_table, back_populates='categories')

    def __init__(self, **kwargs):
        self.category = kwargs.get('category', '')

    def serialize(self):
        return {
            'category': self.category
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)
    selling = db.relationship(
        'Product', foreign_keys='Product.seller_id', cascade='delete')
    buying = db.relationship(
        'Product', foreign_keys='Product.buyer_id', cascade='delete')

    # Session
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.email = kwargs.get('email')
        self.password_digest = bcrypt.hashpw(
            kwargs.get('password').encode('utf8'),
            bcrypt.gensalt(rounds=13)
        )
        self.renew_session()

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'selling': [p.serialize() for p in self.selling],
            'buying': [p.serialize() for p in self.buying]
        }

    def session_serialize(self):
        return {
            'session_token': self.session_token,
            'session_expiration': str(self.session_expiration),
            'update_token': self.update_token
        }

    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password_digest)

    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        return update_token == self.update_token
