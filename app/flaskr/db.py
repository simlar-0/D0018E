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

def create_user(user_type, user):
    """
    """
    query_reg_user = (
        f"""
        INSERT INTO {user_type} (name,email,address,postcode,city)
        VALUES (%s,%s,%s,%s,%s);
        """,
        (
            user['name'],
            user['email'],
            user['address'],
            user['postcode'],
            user['city']))

    query_reg_pass = (
        f"""
        INSERT INTO {user_type}Password (id, hashed_password)
        VALUES (LAST_INSERT_ID(), %s);
        """,
        (user['hashed_password'], )
    )
    return transaction([query_reg_user, query_reg_pass])

def get_user_by_email(user_type, email):
    """
    Gets customer by email address.
    :param user_type: the name of the table that contains the user.
    :param email: the email address.
    :returns a dictionary of the results:
    """
    query = (
        f"""
        SELECT id, name, address, postcode, city
        FROM {user_type}
        WHERE email = %s;
        """,
        (email,))
    results = transaction([query], dict_cursor=True)[0]
    return results[0] if len(results) > 0 else None

def get_user_password(user_type, user_id):
    """
    Gets user by email address.
    :param user_type: the name of the table that contains the user.
    :param user_id: the email address.
    :returns a dictionary of the results:
    """
    query = (
        f"""
        SELECT hashed_password
        FROM {user_type}Password
        WHERE id = %s;
        """,
        (user_id,))
    return transaction([query])[0][0][0]

def get_user_by_id(user_id, user_type):
    """
    Get a user's information.
    
    :param user_id:
    :param user_type: Customer, StoreManager, Admin
    :returns TBD:
    """
    pass

def get_all_products():
    """
    Returns ALL products registered in the DB.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    query = ("""SELECT id, name, description, price, image_path, in_stock FROM Product""", tuple())
    return transaction([query], dict_cursor=True)[0]

def get_some_products(limit, offset):
    """
    Returns <limit> products from the DB, offset by <offset>.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    query = ("""SELECT id, name, description, price, image_path, in_stock FROM Product LIMIT %s OFFSET %s""",
              (limit, offset))
    return transaction([query], dict_cursor=True)[0]

def get_one_product(product_id):
    """
    Returns <limit> products from the DB, offset by <offset>.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    query = ("""SELECT id, name, description, price, image_path, in_stock FROM Product WHERE id=%s""",(product_id,))
    return transaction([query], dict_cursor=True)[0][0]

def count_products():
    """
    Returns the number of products in db.
    :returns: an integer count of products.
    """
    query = ("""SELECT COUNT(*) FROM Product""", tuple())
    return transaction([query])[0][0][0]

def get_cart(customer_id):
    """
    Get the contents of a customer's cart, or create a new cart if non exists.

    :returns: a tuple containing the orderlines and the order_id:
        ([{}], order_id)
    """
    in_cart = get_cart_orderlines(customer_id)
    if in_cart:
        return (in_cart, in_cart[0]['order_id'])
    cart_id = create_cart(customer_id)
    return ([], cart_id)

def get_cart_orderlines(customer_id):
    """
    Get the contents of a customer's cart.
    
    :param customer_id:
    :returns: a list of dictionaries, where each dictionary represents an OrderLine.
    """
    in_cart_query = (
        """
        SELECT
            OrderLine.id, 
            OrderLine.order_id, 
            OrderLine.product_id,
            OrderLine.quantity,
            OrderLine.sub_total_amount,
            OrderLine.unit_price,
            Product.name AS product_name,
            Product.description AS product_description,
            Product.image_path AS product_image_path
        FROM OrderLine
        INNER JOIN Product ON OrderLine.product_id = Product.id
        WHERE OrderLine.order_id = 
        (
            SELECT CustomerOrder.id
            FROM CustomerOrder
            WHERE
                CustomerOrder.order_status_id = 
                    (
                        SELECT OrderStatus.id
                        FROM OrderStatus 
                        WHERE OrderStatus.name = 'InCart'
                    )
            AND
                (CustomerOrder.customer_id = %s)
            LIMIT 1
        );
        """,
        (customer_id,))
    in_cart = transaction([in_cart_query], dict_cursor = True)[0]
    return in_cart

def create_cart(customer_id):
    """
    Create a new cart for a customer and return it (the empty cart). 
        Does NOT check if the customer already has an existing cart.

    :param customer_id:
    :returns: the id of the cart (order)
    """
    create_cart_query = (
        """
        INSERT INTO CustomerOrder (customer_id, total_amount, order_status_id)
        VALUES (
            %s, 
            0, 
            (SELECT OrderStatus.id
            FROM OrderStatus 
            WHERE OrderStatus.name = 'InCart')
        );
        """,
    (customer_id,))
    fetch_cart_id = (
        """
        SELECT LAST_INSERT_ID();
        """,
    tuple())
    cart_id = transaction([create_cart_query, fetch_cart_id])[1][0][0]
    return cart_id

def update_cart(customer_id, product, total_quantity):
    """
    Adds or changes an orderline to / in current order (cart). 
        A 0 quantity will remove the orderline from current order.
    
    :customer_id:
    :param product: a dictionary representation of a product
    :param quantity: an integer
    """
    
    orderlines, cart_id = get_cart(customer_id)

    update_query = lambda orderline_id : (
    """
    UPDATE OrderLine
    SET OrderLine.quantity = %s, OrderLine.sub_total_amount = %s
    WHERE OrderLine.id = %s;
    """
    ,
    (
        total_quantity,
        total_quantity*product['price'],
        orderline_id
    ))

    insert_query = (
    """
    INSERT INTO OrderLine (order_id, product_id, quantity, sub_total_amount, unit_price)
    VALUES (%s, %s, %s, %s, %s);
    """
    ,
    (
        cart_id,
        product['id'],
        total_quantity,
        total_quantity*product['price'],
        product['price']
    ))

    for orderline in orderlines:
        if orderline['product_id'] == product['id']:
            transaction([update_query(orderline['id'])])
            return
    transaction([insert_query])

def get_amount_in_cart(customer_id, product_id):
    """
    Returns the amount of copies of the given product in the cart of a given customer.

    :param customer_id:
    :param product_id:
    :returns: an integer
    """
    orderlines, _ = get_cart(customer_id)
    for orderline in orderlines:
        if orderline['product_id'] == product_id:
            return orderline['quantity']
    return 0