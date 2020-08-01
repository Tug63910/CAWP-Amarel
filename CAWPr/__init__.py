import os
from flask import Flask
from CAWPr.CAWPspider.CAWPspider.spiders.gs_utils import upload_blob

def create_app(test_config=None):
	#create and config the app
	app=Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
		SECRET_KEY='dev',
	)

	if test_config is None:
		#Load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		#Load the test config if passed in
		app.config.from_mapping(test_config)

	#ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	#a simple page that says Hello
	@app.route("/hello")
	def hello():
		return 'Hello'

	from . import application
	app.register_blueprint(application.bp)
	app.add_url_rule('/',endpoint='index')

	from . import auth
	app.register_blueprint(auth.bp)

	from . import db
	db.init_app(app)

	#Initialize postgreSQL
	#If BLOB=testgae does not exist, create it.
	#If it does exist, empty it.
	BUCKET_NAME="cawp-47548.appspot.com"
	REMOTE_BLOB_NAME="testGAE"
	upload_blob(BUCKET_NAME,"",REMOTE_BLOB_NAME)

	return app

