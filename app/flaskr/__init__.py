import os
from flaskr import store, auth
from flask import Flask
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def _conf(conf, test_config=None, default=None):
    if test_config is not None:
        if conf in test_config.keys():
            return test_config[conf]
    return os.getenv(conf, default)

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST']                = _conf('MYSQL_HOST', test_config, 'localhost')
    app.config['MYSQL_USER']                = _conf('MYSQL_USER', test_config)
    app.config['MYSQL_PASSWORD']            = _conf('MYSQL_PASSWORD', test_config)
    app.config['MYSQL_DB']                  = _conf('MYSQL_DB', test_config)
    app.config['MYSQL_PORT']                = int(_conf('MYSQL_PORT',test_config, 3306))
    app.config['MYSQL_UNIX_SOCKET']         = _conf('MYSQL_UNIX_SOCKET', test_config, '/var/run/mysqld/mysqld.sock')
    app.config['MYSQL_CONNECT_TIMEOUT']     = int(_conf('MYSQL_CONNECT_TIMEOUT',test_config, 30)) 
    app.config['MYSQL_READ_DEFAULT_FILE']   = '/etc/mysql/my.cnf'
    app.config['MYSQL_USE_UNICODE']         = bool(_conf('MYSQL_USE_UNICODE', test_config, True))
    app.config['MYSQL_CHARSET']             = _conf('MYSQL_CHARSET', test_config, 'utf8mb4')
    app.config['MYSQL_SQL_MODE']            = _conf('MYSQL_SQL_MODE',test_config, '')
    app.config['MYSQL_CURSORCLASS']         = _conf('MYSQL_CURSORCLASS',test_config, 'DictCursor')
    app.config['MYSQL_AUTOCOMMIT']          = bool(_conf('MYSQL_AUTOCOMMIT', test_config, True))
    app.config['MYSQL_CUSTOM_OPTIONS']      = _conf('MYSQL_CUSTOM_OPTIONS', test_config, None)
    
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