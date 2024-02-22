"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g
from flaskr.auth import login_required
from flaskr.db.user import get_customer_order_ids
from flaskr.db.store import get_order_orderlines
from flaskr.store import get_order_total_amount



bp = Blueprint("customer", __name__, url_prefix="/user")


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
    order_ids    = get_customer_order_ids(g.user['id'])
    order_items = [get_order_orderlines(order_id) for order_id in order_ids]
    total_amount = [get_order_total_amount(order_item) for order_item in order_items]
    return render_template("customer/view_orders.html", order_items=order_items, total_amount=total_amount)
