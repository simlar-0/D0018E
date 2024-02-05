import os
from flaskr import store, auth
from flask import Flask
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')  # MySQL server host
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')  # MySQL username
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')  # MySQL password
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') if test_config is None else test_config['MYSQL_DB']  # MySQL database name
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))  # MySQL server port
    app.config['MYSQL_UNIX_SOCKET'] = os.getenv('MYSQL_UNIX_SOCKET', '/var/run/mysqld/mysqld.sock')  # MySQL Unix socket file path
    app.config['MYSQL_CONNECT_TIMEOUT'] = int(os.getenv('MYSQL_CONNECT_TIMEOUT', 30))  # MySQL connection timeout   
    app.config['MYSQL_READ_DEFAULT_FILE'] = '/etc/mysql/my.cnf'
    app.config['MYSQL_USE_UNICODE'] = bool(os.getenv('MYSQL_USE_UNICODE', True))
    app.config['MYSQL_CHARSET'] = os.getenv('MYSQL_CHARSET', 'utf8mb4')
    app.config['MYSQL_SQL_MODE'] = os.getenv('MYSQL_SQL_MODE', '')
    app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS', 'DictCursor')
    app.config['MYSQL_AUTOCOMMIT'] = bool(os.getenv('MYSQL_AUTOCOMMIT', True))
    app.config['MYSQL_CUSTOM_OPTIONS'] = os.getenv('MYSQL_CUSTOM_OPTIONS', None)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # apply the blueprints to the app
    #app.register_blueprint(auth.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(auth.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

# flask --app flaskr run --debug