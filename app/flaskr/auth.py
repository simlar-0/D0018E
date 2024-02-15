from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_user_by_email, get_user_password

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    return render_template("auth/register.html")


@bp.route("/login")
def login():
    return render_template("auth/login.html")

@auth.route('/login', methods=('POST'))
def login_user():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')

    user = get_user_by_email(email)
    
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))

@bp.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_pass.html")


@bp.route("/logout")
def logout():
    pass