#!/usr/bin/env python

from mtg_search.api_keys import add_primary_key, remove_primary_key, list_primary_keys, list_derived_keys, validate_key
from mtg_search.scripts import mongo, config
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')

# Add Key
parser_add = subparsers.add_parser('add')
parser_add.add_argument('key', help='The new base api key to add')

# Remove Key
parser_remove = subparsers.add_parser('remove')
parser_remove.add_argument('key', help='The base api key to remove')
parser_remove.add_argument('-d', '--derived_keys', help='Also remove all keys derived from this base key', action='store_true')

# List Keys
parser_list = subparsers.add_parser('list')

# Clean up expired derived keys
parser_list = subparsers.add_parser('clean')

args = parser.parse_args()
cmd = args.subcommand


def keys():
    return getattr(mongo.db, config['KEYS_COLL_NAME'])


if cmd == 'add':
    add_primary_key(keys(), args.key)
elif cmd == 'remove':
    remove_primary_key(keys(), args.key, args.derived_keys)
elif cmd == 'list':
    for key in list_primary_keys(keys()):
        print key
elif cmd == 'clean':
    for key in list_derived_keys(keys()):
        validate_key(keys(), key)
