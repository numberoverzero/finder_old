from mtg_search.util import timeutil
from mtg_search.pbkdf2 import pbkdf2
from mtg_search import app

DERIVED_KEY_LIFETIME = int(app.config['DERIVED_KEY_LIFETIME'])
DERIVED_KEY_LENGTH = int(app.config['DERIVED_KEY_LENGTH'])
PRIMARY = 'primary'
DERIVED = 'derived'


def _get_primary_key(keys, key):
    return keys.find_one({'key': key, 'type': PRIMARY})


def has_primary_key(keys, key):
    return bool(_get_primary_key(keys, key))


def add_primary_key(keys, key):
    if not has_primary_key(keys, key):
        key = {'key': key, 'type': PRIMARY}
        keys.insert(key)


def remove_primary_key(keys, key, remove_derived=True):
    primary = _get_primary_key(keys, key)
    if not primary:
        return
    keys.remove(primary)

    if not remove_derived:
        return
    for derived_key in keys.find({'type': DERIVED}):
        computed_key, salt = pbkdf2(key, salt=derived_key['salt'])
        if computed_key == derived_key['key']:
            keys.remove(derived_key)


def list_primary_keys(keys):
    return [i['key'] for i in keys.find({'type': PRIMARY})]


def list_derived_keys(keys):
    return [i['key'] for i in keys.find({'type': DERIVED})]


def derive_key(keys, key, duration=DERIVED_KEY_LIFETIME):
    if not has_primary_key(keys, key):
        return None, None
    utc_expiration = timeutil.utcnow(seconds=duration)
    expiration = timeutil.utc_asint(utc_expiration)
    derived_key, salt = pbkdf2(key, key_len=DERIVED_KEY_LENGTH)
    key = {'key': derived_key, 'salt': salt, 'type': DERIVED, 'exp': expiration}
    keys.insert(key)
    return derived_key, salt


def validate_key(keys, key):
    key = keys.find_one({'key': key})
    if not key:
        return False
    expiration = key.get('exp', None)
    if not expiration:
        return True
    now = timeutil.utc_asint(timeutil.utcnow())
    if now > expiration:
        keys.remove(key)
        return False
    return True


def get_derived_key(keys, key):
    return keys.find_one({'key': key, 'type': DERIVED})


def get_derived_key_expiration(keys, key):
    key = get_derived_key(keys, key)
    return key['exp'] if key else None
