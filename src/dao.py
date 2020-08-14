from db import db, Product, Category
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = api_key = os.environ.get('SENDGRID_API_KEY')


def get_all_products():
    serialized_products = []
    for product in Product.query.all():
        serialized_product = product.serialize()
        serialized_product['categories'] = [c.serialize()
                                            for c in product.categories]
        serialized_products.append(serialized_product)
    return serialized_products


def create_product(name, description, condition, price, sold, categories, seller_id):
    new_product = Product(
        name=name,
        description=description,
        condition=condition,
        price=price,
        sold=sold,
        seller_id=seller_id
    )

    new_product.categories = []
    categories = [c.strip() for c in categories.split(',')]
    for category in categories:
        category = _get_or_create_category(category)
        new_product.categories.append(category)

    db.session.add(new_product)
    db.session.commit()

    serialized_product = new_product.serialize()
    serialized_product['categories'] = [c.serialize()
                                        for c in new_product.categories]
    return serialized_product


def get_product_by_id(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return None
    serialized_product = product.serialize()
    serialized_product['categories'] = [c.serialize()
                                        for c in product.categories]
    return serialized_product


def delete_product_by_id(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return None
    db.session.delete(product)
    db.session.commit()
    serialized_product = product.serialize()
    serialized_product['categories'] = [c.serialize()
                                        for c in product.categories]
    return serialized_product


def buy_product(product_id, buyer_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return None
    buyer = User.query.filter_by(id=buyer_id).first()
    seller = User.query.filter_by(id=product.seller_id).first()

    product.buyer_id = buyer_id
    product.sold = True
    db.session.commit()

    _send_confirmation_email(buyer.username, buyer.email,
                             seller.username, product.name)

    serialized_product = product.serialize()
    serialized_product['categories'] = [c.serialize()
                                        for c in product.categories]
    return serialized_product


def get_all_categories():
    serialized_categories = []
    for category in Category.query.all():
        serialized_category = category.serialize()
        serialized_category['products'] = [p.serialize()
                                           for p in category.products]
        serialized_categories.append(serialized_category)
    return serialized_categories


def get_category_by_id(id):
    category = Category.query.filter_by(id=id).first()
    if Category is None:
        return None
    serialized_category = category.serialize()
    serialized_category['products'] = [p.serialize()
                                       for p in category.products]
    return serialized_category


def _get_or_create_category(cat):
    category = Category.query.filter_by(category=cat).first()
    if category is not None:
        return category
    category = Category(category=cat)
    db.session.commit()
    return category


def _send_confirmation_email(buyer_name, buyer_email, seller_name, product_name):
    content = '<strong>Hi %s, </strong> <br><br>You have successfully made your transation with %s for item: %s. <br><br>Thanks for using Sello' % (
        buyer_name, seller_name, product_name)
    print('content' + content)
    message = Mail(
        from_email='haiyingweng@gmail.com',
        to_emails=buyer_email,
        subject='Thanks for your transaction with Sello',
        html_content=content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(str(e))
