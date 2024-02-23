"""
User-related DB functions and queries.
"""
from flaskr.db.db import transaction

def create_user(user_type, user):
    """
    Create a new user in the DB.

    :param user_type: a string matching the exact name of a table in the DB:
        "Customer" / "Admin" / "StoreManager"
    :param user: a dictionary containing
            {'name':string,
            'email':string,
            'address':string,
            'postcode':string,
            'city':string}
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
        SELECT id, name, address, postcode, city, email
        FROM {user_type}
        WHERE email = %s;
        """,
        (email,))
    results = transaction([query], dict_cursor=True)[0]
    return results[0] if len(results) > 0 else None

def get_user_password(user_type, user_id):
    """
    Gets user password.
    :param user_type: the name of the table that contains the user.
    :param user_id: the user id.
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

def set_user_password(user_type, user_id, hashed_password):
    """
    Sets user password.
    :param user_type: the name of the table that contains the user.
    :param user_id: the email address.
    """
    query = (
        f"""
        UPDATE {user_type}Password
        SET hashed_password = %s
        WHERE id = %s;
        """,
        (hashed_password, user_id)
    )
    transaction([query])
    
def set_user_details(name, email, address, postcode, city, user_id):
    """
    Sets user details.
    :param name: the name of the user.
    :param email: the email address.
    :param address: the address of the user.
    :param postcode: the postcode of the user.
    :param city: the city of the user.
    :param user_id: the user id.
    """
    query = (
        f"""
        UPDATE Customer
        SET name = %s, email = %s, address = %s, postcode = %s, city = %s
        WHERE id = %s;
        """,
        (name, email, address, postcode, city, user_id)
    )
    transaction([query])

def get_user_by_id(user_id, user_type):
    """
    Get a user's information.
    
    :param user_id:
    :param user_type: Customer, StoreManager, Admin
    :returns TBD:
    """
    pass

def edit_user_password(user_type, user):
    """
    Change the password of a user in the database.
    :param user_type: a string matching the exact name of a table in the DB:
        "Customer" / "Admin" / "StoreManager"
    :param user: a dictionary containing
            {'name':string,
            'email':string,
            'address':string,
            'postcode':string,
            'city':string}
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

def get_all_users(user_type):
    """
    Get all users of a certain type.
    :param user_type: the type of user to get.
    :returns a list of dictionaries of the results:
    """
    query = (
        f"""
        SELECT id, name, email, address, postcode, city
        FROM {user_type};
        """,
        ())
    return transaction([query], dict_cursor=True)[0]
