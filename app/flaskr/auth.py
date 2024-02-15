from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import get_user_by_email, get_user_password

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("auth/register.html")

@bp.route("/customer_login")
def login():
    return render_template("auth/customer_login.html")

@bp.route('/customer_login', methods=['POST'])
def login_user():
    email       = request.form.get('email')
    password    = request.form.get('password')

    user        = get_user_by_email('Customer', email)

    if 'id' in user.keys():
        user_pass = get_user_password('Customer', user['id'])
        if check_password_hash(user_pass, password):
            session['user_id'] = user
            session.modified     = True
            return redirect(url_for('auth.user_profile'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login_user'))


@bp.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_pass.html")

@bp.route("/user-profile")
def user_profile():
    return render_template("auth/user_profile.html")

@bp.route("/logout")
def logout():
    session.pop('user_id', None)
    g.pop('user_id', None)

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = session['user_id']

"""
# log in user
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


# protect view
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


# log out user
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.route('/StudentLogin', methods=['GET', 'POST'])
def StudentLogin():

    username = request.form.get("username")
    password = request.form.get("password")
    
    session['username'] = username  # set the cookie  <---

    if (username == 'Atheer' and password == '10') or (username == 'username' and password == 'password') or (username == 'Yahya' and password == '30'):
        # studentname = LoginTable(username, password)
        # db.session.add(studentname)
        # db.session.commit()
        return redirect(url_for('StudentPage'))
    else:
        return render_template("StudentLogin.html")

@app.route('/StudentPage', methods=['GET', 'POST'])
def StudentPage():
    username = session.get('username')  # get the cookie  <---
    return '<h1>welcome ' + username + '</h1>'

"""