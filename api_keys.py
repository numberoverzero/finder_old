import boto.dynamodb


from mtg_search.util import timeutil
from mtg_search.pbkdf2 import pbkdf2
from mtg_search import app

DERIVED_KEY_LIFETIME = int(app.config['DERIVED_KEY_LIFETIME'])
DERIVED_KEY_LENGTH = int(app.config['DERIVED_KEY_LENGTH'])

_conn = boto.dynamodb.connect_to_region(
    app.config['DYNAMODB_REGION'],
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)
dk_table = _conn.get_table(app.config['DERIVED_KEY_TABLE'])
pk_table = _conn.get_table(app.config['PRIMARY_KEY_TABLE'])


def _get_primary_key(key):
    try:
        return pk_table.get_item(hash_key=key)
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None


def has_primary_key(key):
    return bool(_get_primary_key(key))


def add_primary_key(key):
    if not has_primary_key(key):
        pk_table.new_item(hash_key=key).put()


def remove_primary_key(key):
    item = _get_primary_key(key)
    if item:
        item.delete()


def list_primary_keys():
    return [i['key'] for i in pk_table.scan()]


def derive_key(key, duration=DERIVED_KEY_LIFETIME):
    invalidate_derived_key(key)
    utc_expiration = timeutil.utcnow(minutes=duration)
    expiration = timeutil.utc_asint(utc_expiration)
    derived_key, salt = pbkdf2(key, key_len=DERIVED_KEY_LENGTH)
    item = dk_table.new_item(
        hash_key=derived_key,
        attrs={
            'e': expiration,
            's': salt
        }
    )
    item.put()
    return derived_key, salt


def invalidate_derived_key(primary_key):
    for item in dk_table.scan():
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
        dk_table.get_item(hash_key=key).delete()
        return False
    return True


def get_derived_key_expiration(key):
    try:
        return dk_table.get_item(hash_key=key)['e']
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None
