from db import db, User


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def get_user_by_session_token(session_token):
    return User.query.filter(User.session_token == session_token).first()


def get_user_by_update_token(update_token):
    return User.query.filter(User.update_token == update_token).first()


def verify_credentials(email, password):
    option_user = get_user_by_email(email)

    if not option_user:
        return False, option_user

    return option_user.verify_password(password), option_user


def create_user(username, email, password):
    option_user = get_user_by_email(email)

    if option_user:
        return False, option_user

    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return True, user


def renew_session(update_token):
    user = get_user_by_update_token(update_token)

    if not user:
        raise Exception('Invalid update token')

    user.renew_session()
    db.session.commit()
    return user
