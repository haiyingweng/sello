import json
from flask import Flask, request
from db import db
import dao
import user_dao

app = Flask(__name__)
db_filename = "sello.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def extract_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return False, failure_response('Missing authorization header')

    bearer_token = auth_header.replace('Bearer ', '').strip()
    if not bearer_token:
        return False, failure_response('Missing authorization header')

    return True, bearer_token


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
    success, session_token = extract_token(request)

    if not success:
        return session_token

    user = user_dao.get_user_by_session_token(session_token)

    if not user or not user.verify_session_token(session_token):
        return failure_response('Invalid session token')

    user = user.serialize()
    print(user)
    print(user['id'])
    body = json.loads(request.data)
    course = dao.create_product(
        name=body.get('name'),
        description=body.get('description'),
        condition=body.get('condition'),
        price=body.get('price'),
        sold=False,
        categories=body.get('categories'),
        seller_id=user['id']
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


@app.route('/register/', methods=['POST'])
def register_user():
    body = json.loads(request.data)
    username = body.get('username')
    email = body.get('email')
    password = body.get('password')

    if not email or not password or not username:
        return failure_response('Username, email, or password is missing')

    created, user = user_dao.create_user(username, email, password)

    if not created:
        return failure_response('User already exists')

    return success_response({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    })


@app.route('/login/', methods=['POST'])
def login():
    body = json.loads(request.data)
    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return failure_response('Email or password is missing')

    success, user = user_dao.verify_credentials(email, password)

    if not success:
        return failure_response('Email or password is incorrect')

    return success_response({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    })


@app.route('/session/', methods=['POST'])
def update_session():
    success, update_token = extract_token(request)

    if not success:
        return update_token

    try:
        user = user_dao.renew_session(update_token)
    except:
        failure_response('Invalid update token')

    return success_response({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    })


@app.route('/user/')
def current_user():
    success, session_token = extract_token(request)

    if not success:
        return session_token

    user = user_dao.get_user_by_session_token(session_token)

    if not user or not user.verify_session_token(session_token):
        return failure_response('Invalid session token')

    return success_response(user.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
