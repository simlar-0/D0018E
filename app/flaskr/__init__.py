import os
from flaskr import store, auth, customer
from flask import Flask
from dotenv import load_dotenv

load_dotenv(verbose=True,override=True)

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
    app.config['MYSQL_UNIX_SOCKET']         = _conf('MYSQL_UNIX_SOCKET', test_config, None)
    app.config['MYSQL_CONNECT_TIMEOUT']     = int(_conf('MYSQL_CONNECT_TIMEOUT',test_config, 30)) 
    app.config['MYSQL_READ_DEFAULT_FILE']   = '/etc/mysql/my.cnf'
    app.config['MYSQL_USE_UNICODE']         = bool(_conf('MYSQL_USE_UNICODE', test_config, True))
    app.config['MYSQL_CHARSET']             = _conf('MYSQL_CHARSET', test_config, 'utf8mb4')
    app.config['MYSQL_SQL_MODE']            = _conf('MYSQL_SQL_MODE',test_config, '')
    app.config['MYSQL_AUTOCOMMIT']          = bool(_conf('MYSQL_AUTOCOMMIT', test_config, False))
    app.config['MYSQL_CUSTOM_OPTIONS']      = _conf('MYSQL_CUSTOM_OPTIONS', test_config, None)
    app.config['MYSQL_TIME_ZONE']           = _conf('MYSQL_TIME_ZONE', test_config, '+01:00')

    app.config['TESTING']                   = True if test_config is not None else False
    app.config['DEBUG']                     = _conf('DEBUG',test_config, False)

    app.secret_key                          = bytes(_conf('AUTH_KEY',test_config, ''), 'utf-8')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # apply the blueprints to the app
    #app.register_blueprint(auth.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

# flask --app flaskr run --debug