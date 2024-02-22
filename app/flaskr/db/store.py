"""
Store-related DB functions and queries.
"""
from flaskr.db.db import transaction

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

def get_cart_id(customer_id):
    """
    Get the cart id of the specified customer.

    :param customer_id:
    :returns: an integer or None 
    """
    query = (
    """
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
    LIMIT 1;
    """,
    (customer_id,))
    cart_id = transaction([query])[0]
    if cart_id:
        return cart_id[0][0]
    return None


def get_cart_orderlines(customer_id):
    """
    Get the contents of a customer's cart.
    
    :param customer_id:
    :returns: a list of dictionaries, where each dictionary represents an OrderLine
        (with added relevant product information).
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
        INSERT INTO CustomerOrder (customer_id, order_status_id)
        VALUES (
            %s, 
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

def remove_from_cart(orderline_id):
    """
    Removes the specified orderline from the DB

    :param orderline_id:
    """
    query = (
        """
        DELETE FROM OrderLine
        WHERE OrderLine.id = %s;
        """,
    (orderline_id,))
    transaction([query])

def update_cart(customer_id, products, quantities):
    """
    Adds or changes an orderline to / in current order (cart). 
        A 0 quantity will remove the orderline from current order.
    
    :customer_id:
    :param products: a list of dictionaries representing products
    :param total_quantities: a list of integers
    """
    cart_id = get_cart_id(customer_id)
    orderlines = get_cart_orderlines(customer_id)

    update_query = lambda orderline_id, quant, prod : (
    """
    UPDATE OrderLine
    SET OrderLine.quantity = %s, OrderLine.sub_total_amount = %s
    WHERE OrderLine.id = %s;
    """
    ,
    (
        quant,
        quant*prod['price'],
        orderline_id
    ))

    insert_query = lambda prod, quant :(
    """
    INSERT INTO OrderLine (order_id, product_id, quantity, sub_total_amount, unit_price)
    VALUES (%s, %s, %s, %s, %s);
    """
    ,
    (
        cart_id,
        prod['id'],
        quant,
        quant*prod['price'],
        prod['price']
    ))

    remove_from_cart_query = lambda oid :(
    """
    DELETE FROM OrderLine
    WHERE OrderLine.id = %s;
    """
    ,
    (oid,))

    queries = []

    for product, quantity in zip(products, quantities):
        for orderline in orderlines:
            if orderline['product_id'] == product['id']:
                if int(quantity) == 0:
                    queries.append(remove_from_cart_query(orderline['id']))
                else:
                    queries.append(update_query(orderline['id'],int(quantity),product))
                break
        else:
                queries.append(insert_query(product,int(quantity)))

    transaction(queries)

def get_amount_in_cart(customer_id, product_id):
    """
    Returns the amount of copies of the given product in the cart of a given customer.

    :param customer_id:
    :param product_id:
    :returns: an integer
    """
    orderlines = get_cart_orderlines(customer_id)
    for orderline in orderlines:
        if orderline['product_id'] == product_id:
            return orderline['quantity']
    return 0

def checkout(customer_id):
    """
    Moves the cart of the customer to previous orders.

    :param customer_id: Customer id
    """
    cart_id = get_cart_id(customer_id)
    query = (
        """
        UPDATE CustomerOrder
        SET CustomerOrder.order_status_id =
        (SELECT OrderStatus.id
        FROM OrderStatus 
        WHERE OrderStatus.name = 'Confirmed')
        WHERE CustomerOrder.id = %s;
        """,
        (cart_id,)
    )
    transaction([query])
    
def get_order_orderlines(order_id):
    """
    Get the contents of an order.
    
    :param order_id: the id of the order.
    :returns: a list of dictionaries, where each dictionary represents an OrderLine
        (with added relevant product information).
    """
    query = (
        """
        SELECT
            OrderLine.id, 
            OrderLine.order_id, 
            OrderLine.product_id,
            OrderLine.quantity,
            OrderLine.sub_total_amount,
            OrderLine.unit_price,
            Product.name AS product_name
        FROM OrderLine
        INNER JOIN Product ON OrderLine.product_id = Product.id
        WHERE OrderLine.order_id = %s;
        """,
        (order_id,)
    )
    return transaction([query], dict_cursor = True)[0]