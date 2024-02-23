"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g
from flaskr.auth import login_required
from flaskr.db.store import get_order_orderlines, get_customer_orders
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
    user = g.user
    customer_orders    = get_customer_orders(g.user['id'])
    if customer_orders:
        order_items = [get_order_orderlines(order['id']) for order in customer_orders]
        total_amounts = [get_order_total_amount(order_item) for order_item in order_items]
        orders = [{'order': order_item, 'total_amount': total_amount, 'order_date': customer_order['order_date'], 'order_status': customer_order['order_status']} for order_item, total_amount, customer_order in zip(order_items, total_amounts, customer_orders)]
        return render_template("customer/view_orders.html", orders=orders, user=user)
    return render_template("customer/view_orders.html", user=user)