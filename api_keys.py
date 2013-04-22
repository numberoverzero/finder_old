from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.dynamodb


from mtg_search.util import strutil, timeutil
from mtg_search.pbkdf2 import pbkdf2
from mtg_search import app

DERIVED_KEY_LIFETIME = int(app.config['DERIVED_KEY_LIFETIME'])
DERIVED_KEY_LENGTH = int(app.config['DERIVED_KEY_LENGTH'])

s3conn = S3Connection(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
bucket = s3conn.get_bucket(app.config['S3_BUCKET'])
primary_key_file = Key(bucket)
primary_key_file.key = app.config['S3_API_KEY_FILE']

dynamoDBconn = boto.dynamodb.connect_to_region(
    app.config['DYNAMODB_REGION'],
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)
table = dynamoDBconn.get_table(app.config['DYNAMODB_TABLE'])


def _load_primary_keys():
    string = primary_key_file.get_contents_as_string()
    return [line.strip() for line in strutil.sanitize(string).split(u'\n')]


def _save_primary_keys(keys):
    string = u'\n'.join(str(key) for key in keys)
    primary_key_file.set_contents_from_string(string)


def add_primary_key(key):
    keys = _load_primary_keys()
    if key not in keys:
        keys.append(key)
        _save_primary_keys(keys)


def remove_primary_key(key):
    keys = _load_primary_keys()
    if key in keys:
        keys.remove(key)
        _save_primary_keys(keys)


def list_primary_keys():
    return _load_primary_keys()


def derive_key(key, duration=DERIVED_KEY_LIFETIME):
    invalidate_derived_key(key)
    utc_expiration = timeutil.utcnow(minutes=duration)
    expiration = timeutil.utc_asint(utc_expiration)
    derived_key, salt = pbkdf2(key, key_len=DERIVED_KEY_LENGTH)
    item = table.new_item(
        hash_key=derived_key,
        attrs={
            'e': expiration,
            's': salt
        }
    )
    item.put()
    return derived_key, salt


def invalidate_derived_key(primary_key):
    for item in table.scan():
        derived_key = item['key']
        salt = item['s']
        calculated_key, salt = pbkdf2(primary_key, key_len=DERIVED_KEY_LENGTH, salt=salt)
        if calculated_key == derived_key:
            item.delete()


def validate_derived_key(key):
    expiration = get_derived_key_expiration(key)
    if not expiration:
        return False
    now = timeutil.utc_asint(timeutil.utcnow())
    if now > expiration:
        table.get_item(hash_key=key).delete()
        return False
    return True


def get_derived_key_expiration(key):
    try:
        return table.get_item(hash_key=key)['e']
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None
