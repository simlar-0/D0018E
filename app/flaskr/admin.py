"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g, request, flash, redirect, url_for, session
from flaskr.auth import login_required
from flaskr.db.store import get_order_orderlines, get_customer_orders
from flaskr.db.user import get_all_users, get_user_by_id
from flaskr.store import get_order_total_amount
import bcrypt


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/customer-list")
def customer_list():
    customers = get_all_users('Customer')
    return render_template("admin/customer_list.html", customers=customers)

@bp.route("/customer/<int:id>/orders")
def customer_orders(id):
    customer_orders    = get_customer_orders(id)
    user = get_user_by_id(id, 'Customer')
    if customer_orders:
        order_items = [get_order_orderlines(order['id']) for order in customer_orders]
        total_amounts = [get_order_total_amount(order_item) for order_item in order_items]
        orders = [{'order': order_item, 'total_amount': total_amount, 'order_date': customer_order['order_date'], 'order_status': customer_order['order_status']} for order_item, total_amount, customer_order in zip(order_items, total_amounts, customer_orders)]
        return render_template("admin/view_customer_orders.html", orders=orders, user=user)
    return render_template("admin/view_customer_orders.html", user=user)