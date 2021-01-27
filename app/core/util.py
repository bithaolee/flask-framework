from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    ''' 加密密码 '''
    return generate_password_hash(password, method='pbkdf2:sha256:1000', salt_length=8)

def validate_password(hashed, input_password):
    ''' 校验密码 '''
    return check_password_hash(hashed, input_password)