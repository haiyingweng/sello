import json
from flask import Flask, request
from db import db
import dao

app = Flask(__name__)
db_filename = "sello.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


@app.route('/')
@app.route('/products/')
def get_products():
    return success_response(dao.get_all_products())


@app.route('/products/', methods=['POST'])
def create_product():
    body = json.loads(request.data)
    course = dao.create_product(
        name=body.get('name'),
        description=body.get('description'),
        condition=body.get('condition'),
        price=body.get('price'),
        sold=False,
        categories=body.get('categories')
    )
    return success_response(course)


@app.route('/products/<int:product_id>/')
def get_product(product_id):
    product = dao.get_product_by_id(product_id)
    if product is None:
        return failure_response("Product not found!")
    return success_response(product)


@app.route('/products/<int:product_id>/', methods=['DELETE'])
def delete_product(product_id):
    product = dao.delete_product_by_id(product_id)
    if product is None:
        return failure_response("Product not found!")
    return success_response(product)


@app.route('/categories/')
def get_categories():
    return success_response(dao.get_all_categories())


@app.route('/categories/<int:category_id>/')
def get_category(category_id):
    category = dao.get_category_by_id(category_id)
    if category is None:
        return failure_response("Category not found!")
    return success_response(category)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
