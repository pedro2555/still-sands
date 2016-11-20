# -*- coding: utf-8 -*-

import os

products = {
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'item_methods': ['GET', 'PATCH', 'DELETE', 'PUT'],
	'allow_unknown': True,
	'transparent_schema_rules': True,
	'additional_lookup':
		{
			'url': 'regex("[\d]+")',
			'field': 'ean13'
		},
	'additional_lookup':
		{
			'url': 'regex("[\w]+")',
			'field': 'description'
		},
	'schema': {
		'ean13': { 
			'type': 'string',
			'required': True,
			'minlength': 13,
			'maxlength': 13,
			'unique': True
		},
		'description': {
			'type': 'string',
			'required': True,
			'minlength': 5,
			'maxlength': 100
		},
		'weight': {
			'type': 'number'
		}
	}
}

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'still-sands-21077')

HATEOAS = False

DOMAIN = {
	'products': products
}
