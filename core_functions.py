import uuid
import hashlib
import boto3
from botocore.exceptions import ClientError

def hash_string(my_string):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + my_string.encode()).hexdigest() + ':' + salt

def check_string(hashed_string, provided_string):
    unhashed_string, salt = hashed_string.split(':')
    return unhashed_string == hashlib.sha256(salt.encode() + provided_string.encode()).hexdigest()



def get_secret(secret_name):

    session = boto3.session.Session()
    client = session.client(service_name = 'secretsmanager', region_name = "us-east-1")

    try:
        get_secret_value_response = client.get_secret_value( SecretId=secret_name )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return secret