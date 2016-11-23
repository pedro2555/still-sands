# -*- coding: utf-8 -*-

import os
from eve import Eve
from eve.auth import BasicAuth
from werkzeug.security import check_password_hash
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
import hashlib
import uuid
from flask import current_app

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 5000
    host = '0.0.0.0'


# Authentication logic
class Sha1Auth(BasicAuth):
	def check_auth(self, username, password, allowed_roles, resource, method):
		accounts = app.data.driver.db['accounts']
		account = accounts.find_one({
			'email': username
			})
		if account and '_id' in account:
			self.set_request_auth_value(account['_id'])
		return account and \
			hashlib.sha1(account['salt'] + password).hexdigest() == \
			account['password']


app = Eve(auth=Sha1Auth)

# Generates salt and hashes password for storing
def on_insert_accounts_callback(items):
	i = 0
	for item in items:
		items[i]['salt'] = hashlib.sha1(str(os.urandom(64))).hexdigest()
		items[i]['password'] = hashlib.sha1(items[i]['salt'] + items[i]['password']).hexdigest() 
		i += 1
		pass
app.on_insert_accounts += on_insert_accounts_callback

# Updates auth_field to limit every user's scope on the accounts table to their own account entry
def on_inserted_accounts_callback(items):
	accounts = app.data.driver.db['accounts']
	i = 0
	for item in items:
		accounts.update(
			{ '_id': items[i]['_id']},
			{ '$set': { 'account_id': items[i]['_id']}})
		i += 1
		pass
app.on_inserted_accounts += on_inserted_accounts_callback

def pre_accounts_get_callback(request, lookup):
	lookkup = { '_id': current_app.auth.get_request_auth_value() }
	return
app.on_pre_GET_accounts += pre_accounts_get_callback

if __name__ == '__main__':
	Bootstrap(app)
	app.register_blueprint(eve_docs, url_prefix='/docs')

	app.run(host=host, port=port, debug=True)