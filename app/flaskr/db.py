"""
Functions for abstracting communication with the database.
"""
import mysql.connector
from flask import g, current_app

def mysql_settings():
    """
    Get the MySQL settings of the current app context.
    :returns a dictionary:
    """
    app = current_app
    return {
    'user':app.config['MYSQL_USER'],
    'password':app.config['MYSQL_PASSWORD'],
    'database':app.config['MYSQL_DB'],
    'host':app.config['MYSQL_HOST'],
    'unix_socket':app.config['MYSQL_UNIX_SOCKET'],
    'port':app.config['MYSQL_PORT'],
    'autocommit':app.config['MYSQL_AUTOCOMMIT'],
    'sql_mode':app.config['MYSQL_SQL_MODE'],
    'connection_timeout':app.config['MYSQL_CONNECT_TIMEOUT']}

def init_mysql():
    """
    Singelton for MySQL connector.
    :returns a MySQL connector object:
    """

    if 'mysql_conn' not in g:
        g.mysql_conn = mysql.connector.connect(**mysql_settings())
    return g.mysql_conn

def execute_script(script_path):
    """
    Executes .sql script.
    """
    mysql = init_mysql()
    cursor = mysql.cursor()
    try:
        with open(script_path, "rb") as f:
            lines = f.read().decode("utf-8-sig").split(';')
        for line in lines:
            if line.strip() != '':
                cursor.execute(line +';')
            mysql.commit()
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
        queries.append(table[0])
    queries.append("SET FOREIGN_KEY_CHECKS = 1;")
    manipulate_db(queries)

def manipulate_db(queries):
    """
    Perform queries that manipulate DB data.
    :param queries: a list of strings.
    :returns: True if all queries were executed successfully.
    """
    mysql = init_mysql()
    cursor = mysql.cursor()
    try:
        for query in queries:
            cursor.execute(_sanitize(query))
        mysql.commit()
    finally:
        cursor.close()

    # TODO check if queries executed succesfully or not and return False
    return True

def query_db(queries, dict_cursor = False):
    """
    Perform queries that select data from the DB.
    :param queries: a list of strings.
    :param dict_cursor: if True then query results will be a dictionary instead of a list.
    :returns: a list of lists (one per query) of strings.
    """
    results = []

    mysql = init_mysql()
    cursor = mysql.cursor(dictionary=dict_cursor)
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
    return query_db(queries, dict_cursor=True)[0]

def get_some_products(limit, offset):
    """
    Returns <limit> products from the DB, offset by <offset>.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    queries = [f"""SELECT name, description, price, image_path, in_stock FROM Product LIMIT {limit} OFFSET {offset}"""]
    return query_db(queries, dict_cursor=True)[0]

def count_products():
    """
    Returns the number of products in db.
    :returns: an integer count of products.
    """
    queries = [f"""SELECT COUNT(*) FROM Product"""]
    r = query_db(queries)
    return query_db(queries)[0][0][0]