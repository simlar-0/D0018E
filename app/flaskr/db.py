from flask import Flask, g, current_app
from flask_mysqldb import MySQL
import sys

""" MYSQL EXAMPLE (executing queries):
mysql = MySQL(app)
 
#Creating a connection cursor
cursor = mysql.connection.cursor()
 
#Executing SQL Statements
cursor.execute(''' CREATE TABLE table_name(field1, field2...) ''')
cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
cursor.execute(''' DELETE FROM table_name WHERE condition ''')
 
#Saving the Actions performed on the DB
mysql.connection.commit()
 
#Closing the cursor
cursor.close()
"""

def init_db():
    """
    """
    if 'mysql' not in g:
        app = Flask('flaskr')
        g.mysql = MySQL(app)

def get_db(): 
    """This function will probably not be needed, 
    leaving it here just because some other functions 
    (which will also be changed) call for it
    """
    return None

def manipulate_db(queries):
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
    init_db()
    results = []

    mysql = g.mysql
    cursor = mysql.connection.cursor()

    for query in queries:
        #cursor.execute(_sanitize(query))
        cursor.execute(query)
        results.append(cursor.fetchall())
    
    cursor.close()
    return results

def _sanitize(query):
    #TODO
    return query

def get_all_products():
    queries = ["""SELECT name, description, price, imagepath, instock FROM product"""]
    return query_db(queries)[0]

def get_some_products(limit, offset):
    queries = [f"""SELECT name, description, price, imagepath, instock FROM product LIMIT {limit} OFFSET {offset}"""]
    return query_db(queries)[0]

def count_products():
    queries = [f"""SELECT COUNT(*) FROM product"""]
    return query_db(queries)[0][0]['COUNT(*)']