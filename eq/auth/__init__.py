from flask_jwt import JWT
import bcrypt

from .. model.user import User

def authenticate_username(username, password):
    user = User.select().where(User.username == username).first()

    if not user:
        return False
    
    return authenticate(user, password)

def authenticate_id(id, password):
    user = User.select().where(User.id == id).first()

    if not user:
        return False

    return authenticate(user, password)

def authenticate(user, password):
    # return sha256_crypt.encrypt(password) == user.password
    # return user.password == bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return user
    
    return None

def identity(payload):
    user_id = payload['identity']
    user = User.select().where(User.id == user_id).first()
    return user
