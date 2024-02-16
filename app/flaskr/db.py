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
    tables = query_db([query])
    queries = []
    queries.append(("SET FOREIGN_KEY_CHECKS = 0;", set()))
    for table in tables[0]:
        queries.append((table[0], set()))
    queries.append(("SET FOREIGN_KEY_CHECKS = 1;", set()))
    return query_db(queries)

def query_db(queries, dict_cursor = False):
    """
    Perform queries that select data from the DB.
    :param queries: a list of tuples: (query_string, (binding_variables)).
    :param dict_cursor: if True then query results will be a dictionary instead of a list.
    :returns: a list of lists (one per query) of strings.
    """
    results = []

    mysql = init_mysql()
    cursor = mysql.cursor(dictionary=dict_cursor)
    try:
        for query in queries:
            #print("\n==============\n")
            #print(query[0])
            #print("\n==============\n")
            #print(query[1])
            #print("\n==============\n")
            cursor.execute(query[0], query[1])
            results.append(cursor.fetchall())
        mysql.commit()
    finally:
        cursor.close()
    return results

def create_user(user_type, user):
    """
    """
    query_reg_user = (
        f"""INSERT INTO {user_type} (name,email,address,postcode,city)
        VALUES (%s,%s,%s,%s,%s);""",
        (
            user['name'],
            user['email'],
            user['address'],
            user['postcode'],
            user['city']))
    query_db([query_reg_user])
    query_user_id = ("SELECT LAST_INSERT_ID();",set())
    user_id = query_db([query_user_id])[0][0][0]
    query_reg_pass = (
        f"""
        INSERT INTO {user_type}Password (id, hashed_password)
        VALUES (%s, %s);
        """,
        (user_id, user['hashed_password'])
    )
    return query_db([query_reg_pass])

def get_user_by_email(user_type, email):
    """
    Gets customer by email address.
    :param user_type: the name of the table that contains the user.
    :param email: the email address.
    :returns a dictionary of the results:
    """
    query = ("SELECT id, name, address, postcode, city\n"
        + f"FROM {user_type}\n"
        + "WHERE email = %s;",
        (email,))
    results = query_db([query], dict_cursor=True)[0]
    return results[0] if len(results) > 0 else None

def get_user_password(user_type, user_id):
    """
    Gets user by email address.
    :param user_type: the name of the table that contains the user.
    :param user_id: the email address.
    :returns a dictionary of the results:
    """
    query = ("SELECT hashed_password\n"
             + f"FROM {user_type}Password\n"
             + "WHERE id = %s;",
             (user_id,))
    return query_db([query])[0][0][0]

def get_all_products():
    """
    Returns ALL products registered in the DB.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    query = ("""SELECT name, description, price, image_path, in_stock FROM Product""", set())
    return query_db([query], dict_cursor=True)[0]

def get_some_products(limit, offset):
    """
    Returns <limit> products from the DB, offset by <offset>.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    query = ("""SELECT name, description, price, image_path, in_stock FROM Product LIMIT %s OFFSET %s""",
              (limit, offset))
    return query_db([query], dict_cursor=True)[0]

def count_products():
    """
    Returns the number of products in db.
    :returns: an integer count of products.
    """
    query = ("""SELECT COUNT(*) FROM Product""", set())
    return query_db([query])[0][0][0]