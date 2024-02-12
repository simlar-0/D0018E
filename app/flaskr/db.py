"""
Functions for abstracting communication with the database.
"""
import os
from flask import g, current_app
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

def init_mysql():
    """
    Singelton for the flask_mysqldb MySQL instance.
    """
    if 'mysql' not in g:
        app = current_app
        g.mysql = MySQL(app)

def execute_script(script_path):
    """
    Executes .sql script.
    """
    init_mysql()
    mysql = g.mysql
    cursor = mysql.connection.cursor()
    with open(script_path, "rb") as f:
        lines = f.read().decode("utf-8-sig").split(';')
    for line in lines:
        if line.strip() != '':
            cursor.execute(line +';')
    cursor.commit()
    cursor.close()

def create_db(database_name):
    """
    Creates a database.

    :param database_name: the name of the database to be created.
    """
    query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
    _sudo(manipulate_db,[query])

def destroy_db(database_name):
    """
    WARNING, DESTRUCTIVE ACTION!
    Remove all tables and data from the database.

    :param database_name: the name of the database to be dropped.
    """
    # TODO: remove dangling constraints from the DB called 'mysql'
    # not sure why it doesn't happen automatically
    # when the DB they are referencing is removed
    queries = []
    queries.append(f"DROP DATABASE IF EXISTS {database_name};")
    _sudo(manipulate_db, queries)


def grant_privileges(database_name, username, privilege="ALL PRIVILEGES"):
    """
    Grants username a privilege on database_name through @%
    
    :param database_name: string
    :param username: string
    :param privilege: string 
    """

    queries = []
    queries.append(f"GRANT {privilege} ON {database_name} TO '{username}'@'%';")
    queries.append("FLUSH PRIVILEGES;")
    _sudo(manipulate_db, queries)


def manipulate_db(queries):
    """
    Perform queries that manipulate DB data.
    :param queries: a list of strings.
    :returns: True if all queries were executed successfully.
    """
    init_mysql()
    mysql = g.mysql
    cursor = mysql.connection.cursor()

    for query in queries:
        cursor.execute(_sanitize(query))
    
    mysql.connection.commit()

    cursor.close()

    # TODO check if queries executed succesfully or not and return False
    return True

def query_db(queries):
    """
    Perform queries that select data from the DB.
    :param queries: a list of strings.
    :returns: a list of lists (one per query) of strings.
    """
    init_mysql()
    results = []

    mysql = g.mysql
    cursor = mysql.connection.cursor()

    for query in queries:
        cursor.execute(_sanitize(query))
        results.append(cursor.fetchall())
    
    cursor.close()
    return results

def _sanitize(query):
    """
    Sanitize a query. Should probably be replaced with some library.
    :param query: a string.
    :returns: a string (sanitized query).
    """
    #TODO implement / replace
    return query

def get_all_products():
    """
    Returns ALL products registered in the DB.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    queries = ["""SELECT name, description, price, image_path, in_stock FROM Product"""]
    return query_db(queries)[0]

def get_some_products(limit, offset):
    """
    Returns <limit> products from the DB, offset by <offset>.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    queries = [f"""SELECT name, description, price, image_path, in_stock FROM Product LIMIT {limit} OFFSET {offset}"""]
    return query_db(queries)[0]

def count_products():
    """
    Returns the number of products in db.
    :returns: an integer count of products.
    """
    queries = [f"""SELECT COUNT(*) FROM Product"""]
    return query_db(queries)[0][0]['COUNT(*)']

def _sudo(callback, *args, **kwargs):
    if 'mysql' in g:
        del g.mysql
    app = current_app
    old_user = app.config['MYSQL_USER']
    old_pass = app.config['MYSQL_PASSWORD']
    old_host = app.config['MYSQL_HOST']
    old_db   = app.config['MYSQL_DB']
    app.config['MYSQL_USER']        = 'root'
    app.config['MYSQL_PASSWORD']    = os.getenv('MYSQL_ROOT_PASSWORD')
    app.config['MYSQL_ROOT_HOST']   = '%'
    app.config['MYSQL_DB']          = 'mysql'
    init_mysql()
    callback(*args, **kwargs)

    if 'mysql' in g:
        del g.mysql
    app.config['MYSQL_USER']      = old_user
    app.config['MYSQL_PASSWORD']  = old_pass
    app.config['MYSQL_HOST']      = old_host
    app.config['MYSQL_DB']        = old_db
    init_mysql()
