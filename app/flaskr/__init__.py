import os
from flask_mysqldb import MySQL
from flaskr import auth, store
from flaskr import temp_db_test
from flask import Flask
from flask import g

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST'] = os.environ.get('localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(temp_db_test.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app