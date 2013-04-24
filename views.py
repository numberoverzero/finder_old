from functools import wraps
from flask.ext.restful import Resource, fields, marshal_with, abort
from mtg_search import app, api, mongo
from api_keys import derive_key, validate_derived_key, get_derived_key_expiration
from mtg_search.util import timed


gen_fields = {
    'key': fields.Raw,
    'salt': fields.Raw,
    'expiration': fields.Raw
}


class DerivedKeyGenerate(Resource):
    @marshal_with(gen_fields)
    def get(self, base_key):
        derived_key, salt = derive_key(base_key)
        expiration = get_derived_key_expiration(derived_key)
        return {'key': derived_key, 'salt': salt, 'expiration': expiration}
api.add_resource(DerivedKeyGenerate, '/generate/<string:base_key>')


validate_fields = {
    'key': fields.Raw,
    'valid': fields.Raw,
    'expiration': fields.Raw
}


class ValidateKey(Resource):
    @marshal_with(validate_fields)
    def get(self, derived_key):
        valid = validate_derived_key(derived_key)
        expiration = get_derived_key_expiration(derived_key)
        return {'key': derived_key, 'valid': valid, 'expiration': expiration}
api.add_resource(ValidateKey, '/validate/<string:derived_key>')


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with timed(lambda d: app.logger.info("Checked key in {} seconds".format(d))):
            api_key = kwargs.pop('api_key', None)
            valid = validate_derived_key(api_key)
        if not valid:
            abort(403, message="Unauthenticated call.")
        return func(*args, **kwargs)
    return wrapper


class GetCardIds(Resource):
    @authenticated
    def get(self, card_name):
        # Use mongo.db.cards
        return {'name': card_name, 'ids': ['A', 'B']}

api.add_resource(GetCardIds, '/<string:api_key>/ids/<string:card_name>')
