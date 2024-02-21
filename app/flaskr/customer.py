"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template
from flaskr.auth import login_required



bp = Blueprint("customer", __name__, url_prefix="/user")

# TODO: Require logged in as customer for all routes in this blueprint

@bp.route("/")
@login_required
def profile():
    return render_template("customer/profile.html")

@bp.route("/edit-profile")
@login_required
def edit_profile():
    return render_template("customer/edit_profile.html")

@bp.route("/orders")
@login_required
def view_orders():
    return render_template("customer/view_orders.html")
