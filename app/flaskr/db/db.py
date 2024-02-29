"""
Functions for abstracting communication with the database.
"""
import logging
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
    'connection_timeout':app.config['MYSQL_CONNECT_TIMEOUT'],
    'time_zone':app.config['MYSQL_TIME_ZONE']}

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
    :param script_path: a string
    """
    mysql = init_mysql()
    cursor = mysql.cursor()
    try:
        with open(script_path, "rb") as f:
            lines = f.read().decode("utf-8-sig").split(';')
        for line in lines:
            if line.strip() != '':
                cursor.execute(line +';')
    finally:
        cursor.close()

def clear_db():
    """
    !!!WARNING!!!
    Removes all data from the currently used database schema.
    """
    app = current_app
    query = (
        """
        SELECT concat('DROP TABLE IF EXISTS `', TABLE_NAME, '`;')
        FROM information_schema.tables
        WHERE table_schema = %s;
        """,
        (app.config['MYSQL_DB'],))
    tables = transaction([query])
    queries = []
    queries.append(("SET FOREIGN_KEY_CHECKS = 0;", tuple()))
    for table in tables[0]:
        queries.append((table[0], tuple()))
    queries.append(("SET FOREIGN_KEY_CHECKS = 1;", tuple()))
    return transaction(queries)

def transaction(queries, dict_cursor = False):
    """
    Performs a transaction from a list of queries. Will NOT commit if any transaction fails.
    :param queries: a list of tuples: (query_string, (binding_variables)). 
        Note: it is important to use binding variables, to prevent SQL injection.
    :param dict_cursor: if True then query results will be a dictionary instead of a list.
    :returns: a list of lists (one per query) of strings.
    """
    #logging.getLogger().setLevel(logging.DEBUG)
    results = []

    mysql = init_mysql()
    cursor = mysql.cursor(dictionary=dict_cursor)
    try:
        for query in queries:
            logging.debug("\n==============\n")
            logging.debug(query[0])
            logging.debug("\n==============\n")
            logging.debug(query[1])
            logging.debug("\n==============\n")
            cursor.execute(query[0], query[1])
            results.append(cursor.fetchall())
        mysql.commit()
    finally:
        cursor.close()
    logging.debug(results)
    return results