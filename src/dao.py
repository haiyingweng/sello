from db import db, Product, Category


def get_all_products():
    return [p.serialize() for p in Product.query.all()]


def create_product(name, description, condition, price, sold):
    new_product = Product(
        name=name,
        description=description,
        condition=condition,
        price=price,
        sold=sold
    )
    db.session.add(new_product)
    db.session.commit()
    return new_product.serialize()


def get_product_by_id(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return None
    return product.serialize()


def delete_product_by_id(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return None
    db.session.delete(product)
    db.session.commit()
    return product.serialize()


def get_category_by_id(id):
    category = Category.query.filter_by(id=id).first()
    if Category is None:
        return None
    return category.serialize()
