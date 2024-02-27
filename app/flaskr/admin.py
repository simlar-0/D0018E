"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g
from flaskr.db.store import get_order_orderlines, get_customer_orders
from flaskr.db.user import get_all_users, get_user_by_id
from flaskr.store import get_order_total_amount
from flaskr.auth import manager


bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/")
@manager
def index():
    return render_template("admin/index.html", manager=g.manager)

@bp.route("/customer-list")
@manager
def customer_list():
    """
    Retrieve a list of customers and render it in the customer_list.html template.

    :returns The rendered template with the list of customers:
    """
    customers = get_all_users('Customer')
    return render_template("admin/customer_list.html", customers=customers)

@bp.route("/customer/<int:id>/orders")
@manager
def customer_orders(id):
    """
    Retrieve the orders of a customer with the given ID.

    :param id: The ID of the customer.

    :returns The rendered template containing the customer's orders:
    """
    customer_orders = get_customer_orders(id, with_cart= True)
    user = get_user_by_id(id, 'Customer')
    if customer_orders:
        order_items = [get_order_orderlines(order['id']) for order in customer_orders]
        total_amounts = [get_order_total_amount(order_item) for order_item in order_items]
        orders = [{'order': order_item, 'total_amount': total_amount, 'order_date': customer_order['order_date'], 'order_status': customer_order['order_status']} for order_item, total_amount, customer_order in zip(order_items, total_amounts, customer_orders)]
        return render_template("admin/view_customer_orders.html", orders=orders, user=user)
    return render_template("admin/view_customer_orders.html", user=user)