#!/usr/bin/env python

from mtg_search.api_keys import add_primary_key, remove_primary_key, list_primary_keys
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')

# Add Key
parser_add = subparsers.add_parser('add')
parser_add.add_argument('key', help='The new base api key to add')

# Remove Key
parser_remove = subparsers.add_parser('remove')
parser_remove.add_argument('key', help='The base api key to remove')

# List Keys
parser_list = subparsers.add_parser('list')

args = parser.parse_args()
cmd = args.subcommand

if cmd == 'add':
    add_primary_key(args.key)
elif cmd == 'remove':
    remove_primary_key(args.key)
elif cmd == 'list':
    for key in list_primary_keys():
        print key
