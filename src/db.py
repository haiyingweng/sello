from flask_sqlalchemy import SQLAlchemy

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
    categories = db.relationship(
        'Category', secondary=association_table, back_populates='products')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.condition = kwargs.get('condition', '')
        self.price = kwargs.get('price', '')
        self.sold = kwargs.get('sold', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'condition': self.condition,
            'price': self.price,
            'sold': self.sold
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
