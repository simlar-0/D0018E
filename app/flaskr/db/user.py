"""
User-related DB functions and queries.
"""
from flaskr.db.db import transaction

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