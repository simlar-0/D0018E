"""
Functions for abstracting communication with the database.
"""
from flask import Flask, g
from flask_mysqldb import MySQL

def init_db():
    """
    Singelton for the flask_mysqldb MySQL instance.
    """
    if 'mysql' not in g:
        app = Flask('flaskr')
        g.mysql = MySQL(app)

def manipulate_db(queries):
    """
    Perform queries that manipulate DB data.
    :param queries: a list of strings.
    :returns: True if all queries were executed successfully.
    """
    init_db()
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
    init_db()
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