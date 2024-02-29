from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from functools import wraps
from flaskr.db.user import (
    get_customer_by_email, 
    get_user_password, 
    create_customer,
    get_manager_by_email)
import bcrypt

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def manager(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.manager is None:
            return redirect(url_for('auth.login_manager'))
        return f(*args, **kwargs)
    return decorated_function

def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.manager is None:
            return redirect(url_for('auth.login_manager'))
        if not g.manager['is_admin']:
            return redirect(url_for('auth.not_allowed', reason='manager_not_admin'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/not_allowed/<string:reason>")
def not_allowed(reason):
    reasons = {
        'manager_not_admin':"You are logged in as a manager, but must be an admin to access this resource."
    }
    return render_template("auth/not_allowed.html", desc=reasons[reason])

@bp.route("/register")
def register():
    return render_template("auth/register.html")

@bp.route("/register", methods=["POST"])
def register_user():
    forms = request.form.to_dict()

    user = get_customer_by_email(forms['email'])
    if user is not None:
        flash("There is already a user with that email address!")
        return redirect(url_for('auth.register'))
    hashed_pass = bcrypt.hashpw(bytes(forms['password'], 'utf-8'), bcrypt.gensalt())
    user = {
        'name':forms['name'],
        'email':forms['email'],
        'address':forms['address'],
        'city':forms['city'],
        'postcode':forms['postcode'],
        'hashed_password':hashed_pass
    }

    create_customer(user)
    
    user = get_customer_by_email(forms['email'])
    session['user_id'] = user
    session.modified = True
    return redirect(url_for('customer.profile'))

@bp.route("/customer_login")
def login():
    return render_template("auth/customer_login.html")

@bp.route('/customer_login', methods=['POST'])
def login_user():
    email       = request.form.get('email')
    password    = request.form.get('password')
    user        = get_customer_by_email(email)

    if user and 'id' in user.keys():
        pass_from_db = get_user_password('Customer', user['id'])
        if bcrypt.checkpw(bytes(password, 'utf-8'),bytes(pass_from_db.decode(), 'utf-8')):
            session['user_id'] = user
            session.modified     = True
            return redirect(url_for('customer.profile'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login_user'))

@bp.route("/manager_login")
def login_manager():
    return render_template("auth/manager_login.html")

@bp.route('/manager_login', methods=['POST'])
def login_manager_post():
    email       = request.form.get('email')
    password    = request.form.get('password')
    manager     = get_manager_by_email(email)

    if manager and 'id' in manager.keys():
        pass_from_db = get_user_password('Manager', manager['id'])
        if bcrypt.checkpw(bytes(password, 'utf-8'),bytes(pass_from_db.decode(), 'utf-8')):
            session['manager_id'] = manager
            session.modified     = True
            return redirect(url_for('admin.index'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login_manager_post'))

@bp.route("/logout")
def logout():
    session.pop('user_id', None)
    g.pop('user_id', None)
    return redirect(url_for('store.index'))

@bp.route("/manager_logout")
def manager_logout():
    session.pop('manager_id', None)
    g.pop('manager_id', None)
    return redirect(url_for('store.index'))

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    manager_id = session.get("manager_id")

    if user_id is None:
        g.user = None
    else:
        g.user = session['user_id']

    if manager_id is None:
        g.manager = None
    else:
        g.manager = session['manager_id']