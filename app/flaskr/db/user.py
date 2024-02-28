"""
User-related DB functions and queries.
"""
from flaskr.db.db import transaction

def create_manager(manager):
    """
    Create a new manager in the DB.

    :param manager: a dictionary containing
            {'name':string,
            'email':string,
            'hashed_password':bcrypt hash in binary format,
            'is_admin':boolean}
    """
    query_reg_manager = (
        """
        INSERT INTO Manager (is_admin,name,email)
        VALUES (%s,%s,%s);
        """,
        (
            manager['is_admin'],
            manager['name'],
            manager['email']))

    query_reg_pass = (
        """
        INSERT INTO ManagerPassword (id, hashed_password)
        VALUES (LAST_INSERT_ID(), %s);
        """,
        (manager['hashed_password'], )
    )
    return transaction([query_reg_manager, query_reg_pass])

def create_customer(user):
    """
    Create a new Customer in the DB.

    :param user: a dictionary containing
            {'name':string,
            'email':string,
            'address':string,
            'postcode':string,
            'city':string,
            'hashed_password':bcrypt hash in binary format}
    """
    query_reg_user = (
        """
        INSERT INTO Customer (name,email,address,postcode,city)
        VALUES (%s,%s,%s,%s,%s);
        """,
        (
            user['name'],
            user['email'],
            user['address'],
            user['postcode'],
            user['city']))

    query_reg_pass = (
        """
        INSERT INTO CustomerPassword (id, hashed_password)
        VALUES (LAST_INSERT_ID(), %s);
        """,
        (user['hashed_password'], )
    )
    return transaction([query_reg_user, query_reg_pass])

def get_customer_by_email(email):
    """
    Gets customer by email address.
    :param user_type: the name of the table that contains the user.
    :param email: the email address.
    :returns a dictionary of the results:
    """
    query = (
        """
        SELECT id, name, address, postcode, city, email
        FROM Customer
        WHERE email = %s;
        """,
        (email,))
    results = transaction([query], dict_cursor=True)[0]
    return results[0] if len(results) > 0 else None

def get_manager_by_email(email):
    """
    Gets customer by email address.
    :param user_type: the name of the table that contains the user.
    :param email: the email address.
    :returns a dictionary of the results:
    """
    query = (
        """
        SELECT id, name, email, is_admin
        FROM Manager
        WHERE email = %s;
        """,
        (email,))
    results = transaction([query], dict_cursor=True)[0]
    return results[0] if len(results) > 0 else None

def get_user_by_email(user_type, email):
    """
    Gets user by email address.
    :param user_type: the name of the table that contains the user.
    :param email: the email address.
    :returns a dictionary of the results:
    """
    if user_type == 'Customer':
        return get_customer_by_email(email)
    elif user_type == 'Manager':
        return get_manager_by_email(email)
    else:
        return None

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
    
def set_user_details(details, user_id):
    """
    Sets user details.
    :param details: a dictionary containing the details to update. 
        Contains the following keys: name, email, address, postcode, city.
    :param user_id: the user id.
    """
    query = (
        f"""
        UPDATE Customer
        SET name = %s, email = %s, address = %s, postcode = %s, city = %s
        WHERE id = %s;
        """,
        (details['name'], details['email'], details['address'], details['postcode'], details['city'], user_id)
    )
    transaction([query])

def get_user_by_id(user_id, user_type):
    """
    Get a user's information.
    
    :param user_id:
    :param user_type: Customer, StoreManager, Admin
    :returns TBD:
    """
    query = (
        f"""
        SELECT id, name, email, address, postcode, city
        FROM {user_type}
        WHERE id = %s;
        """,
        (user_id,))
    return transaction([query], dict_cursor=True)[0][0]


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

def delete_user(user_id, user_type):
    """
    Delete a user from the database.
    :param user_id: the id of the user to delete.
    :param user_type: the type of user to delete.
    """
    query_delete_user = (
        f"""
        DELETE FROM {user_type}
        WHERE id = %s;
        """,
        (user_id,))
    transaction([query_delete_user])
