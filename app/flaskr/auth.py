from flask import Blueprint, render_template

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    return render_template("auth/login.html")

@bp.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_pass.html")


@bp.route("/logout")
def logout():
    pass