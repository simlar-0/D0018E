from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from functools import wraps
from flaskr.db import get_user_by_email, get_user_password, create_user
import bcrypt

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/register")
def register():
    return render_template("auth/register.html")

@bp.route("/register", methods=["POST"])
def register_user():
    name            = request.form.get('name')
    email           = request.form.get('email')
    address         = request.form.get('address')
    city            = request.form.get('city')
    postcode        = request.form.get('postcode')
    password        = request.form.get('password')

    user = get_user_by_email('Customer', email)
    if user is not None:
        flash("There is already a user with that email address!")
        return redirect(url_for('auth.register'))
    hashed_pass = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    user = {
        'name':name,
        'email':email,
        'address':address,
        'city':city,
        'postcode':postcode,
        'hashed_password':hashed_pass
    }

    create_user('Customer',user)
    session['user_id'] = user
    session.modified     = True
    return redirect(url_for('customer.profile'))

@bp.route("/customer_login")
def login():
    return render_template("auth/customer_login.html")

@bp.route('/customer_login', methods=['POST'])
def login_user():
    email       = request.form.get('email')
    password    = request.form.get('password')
    user        = get_user_by_email('Customer', email)

    if 'id' in user.keys():
        pass_from_db = get_user_password('Customer', user['id'])
        if bcrypt.checkpw(bytes(password, 'utf-8'),bytes(pass_from_db.decode(), 'utf-8')):
            session['user_id'] = user
            session.modified     = True
            return redirect(url_for('customer.profile'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login_user'))


@bp.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_pass.html")

@bp.route("/logout")
def logout():
    session.pop('user_id', None)
    g.pop('user_id', None)
    return redirect(url_for('store.index'))

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = session['user_id']