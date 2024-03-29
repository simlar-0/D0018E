"""
Store-related DB functions and queries.
"""
from flaskr.db.db import transaction
MAX_SUB_TOTAL = 10**16
MAX_QUANTITY = 999

def get_all_products(include_unlisted=False):
    """
    Returns ALL products registered in the DB, with the option to include unlisted.
    
    :param include_unlisted: if True, includes unlisted products.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    if include_unlisted:
        query = ("""
                 SELECT 
                    Product.id,
                    Product.name, 
                    Product.description, 
                    Product.price, 
                    Product.image_path, 
                    Product.in_stock,
                    ProductStatus.name AS product_status 
                FROM 
                    Product
                INNER JOIN ProductStatus ON Product.product_status_id = ProductStatus.id;
                """, tuple())
    else:
        query = ("""
                SELECT 
                    id, name, description, price, image_path, in_stock 
                FROM 
                    Product
                WHERE Product.product_status_id =
                    (
                        SELECT ProductStatus.id
                        FROM ProductStatus 
                        WHERE ProductStatus.name = 'Listed'
                    );
                """, tuple())
    return transaction([query], dict_cursor=True)[0]

def get_some_products(limit, offset, include_unlisted=False):
    """
    Returns <limit> products from the DB, offset by <offset>, with the option to include unlisted.
    :param limit: the number of products to return.
    :param offset: the number of products to skip.
    :param include_unlisted: if True, includes unlisted products.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    if include_unlisted:
        query = ("""
                 SELECT 
                    id, name, description, price, image_path, in_stock 
                 FROM 
                    Product 
                LIMIT %s OFFSET %s;
                """,(limit, offset))
    else:
        query = ("""SELECT 
                        id, name, description, price, image_path, in_stock 
                    FROM 
                        Product 
                    WHERE 
                        Product.product_status_id =
                            (
                                SELECT ProductStatus.id
                                FROM ProductStatus 
                                WHERE ProductStatus.name = 'Listed'
                            ) 
                    LIMIT %s OFFSET %s;
                    """,(limit, offset))
    return transaction([query], dict_cursor=True)[0]

def get_one_product(product_id):
    """
    Returns <limit> products from the DB, offset by <offset>.
    :returns: a list of tuples (name, description, price, image_path, in_stock). 
    """
    query = (
        """
        SELECT 
            Product.id, 
            Product.name, 
            Product.description, 
            Product.price, 
            Product.image_path, 
            Product.in_stock,
            Product.product_status_id,
            ProductStatus.name AS product_status
        FROM Product
        INNER JOIN ProductStatus ON Product.product_status_id = ProductStatus.id
        WHERE Product.id=%s;
        """,
        (product_id,))
    return transaction([query], dict_cursor=True)[0][0]

def count_products(include_unlisted=False):
    """
    Returns the number of products in db.
    :param include_unlisted: if True, includes unlisted products.
    :returns: an integer count of products.
    """
    if include_unlisted:
        query = ("""
                 SELECT 
                    COUNT(*)    
                FROM 
                    Product;
                """, tuple())
    else:
        query = ("""
                SELECT 
                    COUNT(*)    
                FROM 
                    Product 
                WHERE 
                    Product.product_status_id =
                        (
                            SELECT ProductStatus.id
                            FROM ProductStatus 
                            WHERE ProductStatus.name = 'Listed'
                        )
                        """, tuple())
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
            Product.image_path AS product_image_path,
            Product.in_stock AS product_stock
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

def update_cart(customer_id, products, quantities):
    """
    Adds or changes an orderline to / in current order (cart). 
        A 0 quantity will remove the orderline from current order.
    
    :customer_id:
    :param products: a list of dictionaries representing products
    :param total_quantities: a list of integers
    """
    def _get_update_cart_query (orderline_id, quantity, product) : 
        return (
            """
            UPDATE OrderLine
            SET OrderLine.quantity = %s, OrderLine.sub_total_amount = %s
            WHERE OrderLine.id = %s;
            """
            ,
            (
                quantity,
                quantity*product['price'],
                orderline_id
            )
        )

    def _get_insert_to_cart_query (cart_id, product, quantity):
        return (
            """
            INSERT INTO OrderLine (order_id, product_id, quantity, sub_total_amount, unit_price)
            VALUES (%s, %s, %s, %s, %s);
            """
            ,
            (
                cart_id,
                product['id'],
                quantity,
                quantity*product['price'],
                product['price']
            )
        )

    def _get_remove_from_cart_query (order_id):
        return (
            """
            DELETE FROM OrderLine
            WHERE OrderLine.id = %s;
            """
            ,
            (order_id,)
        )

    def _get_stock_change_query(product_id, new_stock):
        return (
            """
            UPDATE Product
            SET Product.in_stock = %s
            WHERE Product.id = %s;
            """,
            (new_stock, product_id)
        )

    cart_id = get_cart_id(customer_id)
    orderlines = get_cart_orderlines(customer_id)

    queries = []

    for product, target_quantity in zip(products, quantities):
        sub_total = int(target_quantity)*product['price']
        if int(target_quantity) > MAX_QUANTITY:
            print(f"Cannot add more than {MAX_QUANTITY} units!")
            continue
        if  sub_total > MAX_SUB_TOTAL:
            print(f"Cannot add something that costs more than {MAX_SUB_TOTAL}")
            continue
        for orderline in orderlines:
            if orderline['product_id'] == product['id']:
                if int(product['in_stock']) - (int(target_quantity) - int(orderline['quantity'])) < 0:
                    break
                queries.append(_get_stock_change_query(
                        product['id'],
                        int(product['in_stock']) - (int(target_quantity) - int(orderline['quantity']))
                        ))
                if int(target_quantity) == 0:
                    queries.append(_get_remove_from_cart_query(orderline['id']))
                else:
                    queries.append(_get_update_cart_query(orderline['id'],int(target_quantity),product))
                break
        else:
            if int(product['in_stock']) - int(target_quantity) < 0:
                continue
            queries.append(_get_insert_to_cart_query(cart_id, product,int(target_quantity)))
            queries.append(_get_stock_change_query(
                    product['id'],
                    int(product['in_stock']) - int(target_quantity)))

    queries.append((
        """
        UPDATE CustomerOrder
        SET CustomerOrder.order_date = NOW()
        WHERE CustomerOrder.id = %s;
        """,
        (cart_id,)
    ))
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
        SET 
            CustomerOrder.order_status_id =
                (SELECT OrderStatus.id
                FROM OrderStatus 
                WHERE OrderStatus.name = 'Confirmed'),
            CustomerOrder.order_date = NOW()
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

def get_customer_orders(customer_id, with_cart):
    """
    Get all orders belonging to the specified customer.

    :param customer_id: Customer id
    :param with_cart: will include the content of the customer's cart if True
    :returns: a list of dictionaries containing keys: id, order_date, order_status
    """
    query = (
        """
        SELECT 
            CustomerOrder.id,
            CustomerOrder.order_date,
            OrderStatus.name AS order_status
        FROM CustomerOrder
        INNER JOIN OrderStatus ON CustomerOrder.order_status_id = OrderStatus.id
        WHERE
            CustomerOrder.customer_id = %s
        ORDER BY CustomerOrder.id DESC;
        """,
        (customer_id,)
    ) if with_cart else (
        """
        SELECT 
            CustomerOrder.id,
            CustomerOrder.order_date,
            OrderStatus.name AS order_status
        FROM CustomerOrder
        INNER JOIN OrderStatus ON CustomerOrder.order_status_id = OrderStatus.id
        WHERE
            CustomerOrder.customer_id = %s
        AND
            CustomerOrder.order_status_id != 
                (SELECT OrderStatus.id
                FROM OrderStatus 
                WHERE OrderStatus.name = 'InCart');
        """,
        (customer_id,)
    )

    orders = transaction([query], dict_cursor = True)[0]
    return orders

def get_product_reviews(product_id):
    """
    Get all reviews for a product. Joined with Customer to get the customer's name.
    
    :param product_id: the id of the product.
    :returns: a list of dictionaries containing keys review, rating, customer_id
    """
    query = (
        """
        SELECT 
            Review.review,
            Review.rating,
            Review.customer_id,
            Review.date,
            Customer.name
        FROM Review
        INNER JOIN Customer ON Review.customer_id = Customer.id
        WHERE Review.product_id = %s;
        """,
        (product_id,)
    )
    return transaction([query], dict_cursor = True)[0]

def add_product_review(produt_id, customer_id, review, rating):
    """
    Add a review to a product.
    
    :param product_id: the id of the product.
    :param customer_id: the id of the customer.
    """
    query = (
        """
        INSERT INTO Review (product_id, customer_id, review, rating, date)
        VALUES (%s, %s, %s, %s, NOW());
        """,
        (produt_id, customer_id, review, rating)
    )
    transaction([query])

    
def update_product(details):
    """
    Update the details of a product.
    
    :param details: a dictionary containing the new details of the product.
    """
    query = (
        """
        UPDATE Product
        SET 
            name = %s,
            description = %s,
            price = %s,
            in_stock = %s,
            image_path = %s,
            product_status_id = (
                SELECT ProductStatus.id
                FROM ProductStatus 
                WHERE ProductStatus.name = %s
            ) 
        WHERE Product.id = %s;
        """,
        (details['name'], details['description'], details['price'], details['stock'], details['image_path'], details['status'], details['id'])
    )
    transaction([query])
    
def add_product(details):
    """
    Add a product to the database.
    """
    query = (
        """
        INSERT INTO 
            Product (
                name, 
                description, 
                price, 
                in_stock, 
                image_path, 
                product_status_id)
        VALUES (%s, %s, %s, %s, %s,
            (
                SELECT ProductStatus.id
                FROM ProductStatus 
                WHERE ProductStatus.name = %s
            ) 
        );
        """,
        (details['name'], details['description'], details['price'], details['stock'], details['image_path'], details['status'])
    )
    transaction([query])

def get_customer_has_reviewed_product(customer_id, product_id):
    """
    Check if a customer has reviewed a product.
    
    :param product_id: the id of the product.
    :param customer_id: the id of the customer.
    :returns: an integer count of reviews.
    """
    query = (
        """
        SELECT 
            COUNT(*)
        FROM Review
        WHERE 
            Review.product_id = %s
        AND
            Review.customer_id = %s;
        """,
        (product_id, customer_id)
    )
    return transaction([query])[0][0][0]

def get_customer_has_ordered_product(customer_id, product_id):
    """
    Check if a customer has ordered a product.
    
    :param customer_id: the id of the customer.
    :param product_id: the id of the product.
    :returns: an integer count of orders.
    """
    query = (
        """
        SELECT 
            COUNT(*) 
        FROM OrderLine
        INNER JOIN CustomerOrder ON OrderLine.order_id = CustomerOrder.id
        WHERE 
            CustomerOrder.customer_id = %s
        AND
            OrderLine.product_id = %s
        AND 
            CustomerOrder.order_status_id !=
                (SELECT OrderStatus.id
                FROM OrderStatus 
                WHERE OrderStatus.name = 'InCart');
        """,
        (customer_id, product_id)
    )
    return transaction([query])[0][0][0]

def get_non_cart_orderlines():
    """
    Fetches all orderlines belonging to 
        pending (not 'InCart') orders in the DB.

    :returns: a list of dictionaries, where each dictionary contains an orderline.
    """
    query = (
        """
        SELECT 
            CustomerOrder.id as order_id,
            customer_id, 
            order_date, 
            order_status_id,
            Customer.name AS customer_name,
            OrderLine.sub_total_amount,
            OrderLine.id as orderline_id,
            OrderLine.product_id,
            OrderLine.quantity,
            OrderLine.unit_price,
            OrderStatus.name as status
        FROM CustomerOrder
        INNER JOIN Customer ON Customer.id = customer_id
        INNER JOIN OrderLine ON OrderLine.order_id = CustomerOrder.id
        INNER JOIN OrderStatus ON OrderStatus.id = CustomerOrder.order_status_id
        WHERE CustomerOrder.order_status_id IN 
        (
            SELECT OrderStatus.id
            FROM OrderStatus
            WHERE OrderStatus.name NOT IN ('InCart')
        )
        ORDER BY CustomerOrder.order_status_id;
        """,
        (tuple()))

    return transaction([query], dict_cursor = True)[0]

def change_order_status(order_id, new_status_id):
    """
    Changes the status of an order in the DB.

    :param order_id:
    :param new_status_id:
    """
    query = (
        """
        UPDATE CustomerOrder 
        SET CustomerOrder.order_status_id = %s
        WHERE CustomerOrder.id = %s;
        """,
        (new_status_id, order_id)
    )
    transaction([query])

def get_non_cart_statuses():
    """
    Get all order statuses and their corresponding ids, except InCart.

    :returns: a list of dictionaries, where each dictionary contains an OrderStatus.
    """
    query = (
        """
        SELECT id, name
        FROM OrderStatus
        WHERE OrderStatus.name != "InCart";
        """,
        (tuple())
    )
    return transaction([query], dict_cursor = True)[0]
