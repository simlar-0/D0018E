from flask_mysqldb import MySQL

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

def get_db(): 
    """This function will probably not be needed, 
    leaving it here just because some other functions 
    (which will also be changed) call for it
    """
    return None