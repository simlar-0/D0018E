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
    Get a DB

    :returns a flaskMySQL object:
    """
    app = current_app
    mysql = MySQL(app)
    return mysql

def execute_script(script_path):
    """
    Executes .sql script.
    """
    mysql = init_mysql()
    cursor = mysql.connection.cursor()
    try:
        with open(script_path, "rb") as f:
            lines = f.read().decode("utf-8-sig").split(';')
        for line in lines:
            if line.strip() != '':
                cursor.execute(line +';')
            mysql.connection.commit()
    finally:
        cursor.close()

def clear_db():
    """
    !!!WARNING!!!
    Removes all data from the currently used database schema.
    """
    app = current_app
    long_query = "SELECT concat('DROP TABLE IF EXISTS `', TABLE_NAME, '`;'\n)"
    long_query += "FROM information_schema.tables\n"
    long_query += f"WHERE table_schema = '{app.config['MYSQL_DB']}';"
    tables = query_db([long_query])
    queries = []
    queries.append("SET FOREIGN_KEY_CHECKS = 0;")
    for table in tables[0]:
        queries.append(list(table.values())[0])
    queries.append("SET FOREIGN_KEY_CHECKS = 1;")
    manipulate_db(queries)

def manipulate_db(queries):
    """
    Perform queries that manipulate DB data.
    :param queries: a list of strings.
    :returns: True if all queries were executed successfully.
    """
    mysql = init_mysql()
    cursor = mysql.connection.cursor()
    try:
        for query in queries:
            cursor.execute(_sanitize(query))
        mysql.connection.commit()
    finally:
        cursor.close()

    # TODO check if queries executed succesfully or not and return False
    return True

def query_db(queries):
    """
    Perform queries that select data from the DB.
    :param queries: a list of strings.
    :returns: a list of lists (one per query) of strings.
    """
    results = []

    mysql = init_mysql()
    cursor = mysql.connection.cursor()
    try:
        for query in queries:
            cursor.execute(_sanitize(query))
            results.append(cursor.fetchall())
    finally:
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