# -*- coding: utf-8 -*-

import os
from eve import Eve
from eve.auth import BasicAuth
from werkzeug.security import check_password_hash
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
import hashlib
import uuid

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 5000
    host = '127.0.0.1'


# Authentication logic
class Sha1Auth(BasicAuth):
	def check_auth(self, username, password, allowed_roles, resource, method):
		accounts = app.data.driver.db['accounts']
		account = accounts.find_one({
			'email': username
			})
		return account and \
			hashlib.sha1(account['salt'] + password).hexdigest() == \
			account['password']


app = Eve(auth=Sha1Auth)

def on_insert_accounts(items):
	i = 0
	for item in items:
		items[i]['salt'] = hashlib.sha1(str(uuid.uuid4())).hexdigest()
		items[i]['password'] = hashlib.sha1(items[i]['salt'] + items[i]['password']).hexdigest()
		i+=1
		pass
app.on_insert_accounts += on_insert_accounts

if __name__ == '__main__':
	Bootstrap(app)
	app.register_blueprint(eve_docs, url_prefix='/docs')

	app.run(host=host, port=port, debug=True)