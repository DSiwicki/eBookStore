import uuid
import hashlib

def hash_string(my_string):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + my_string.encode()).hexdigest() + ':' + salt

def check_string(hashed_string, provided_string):
    unhashed_string, salt = hashed_string.split(':')
    return unhashed_string == hashlib.sha256(salt.encode() + provided_string.encode()).hexdigest()

