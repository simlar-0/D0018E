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
    user = g.user
    order_ids    = get_customer_order_ids(g.user['id'])
    order_items = [get_order_orderlines(order_id) for order_id in order_ids]
    total_amounts = [get_order_total_amount(order_item) for order_item in order_items]
    orders = [dict(zip(['order', 'total_amount'], order)) for order in zip(order_items, total_amounts)]
    #[{'order': [{'id': 1, 'order_id': 1, 'product_id': 7, 'quantity': 34, 'sub_total_amount': Decimal('15300.00'), 'unit_price': Decimal('450.00'), 'product_name': 'Ultra-White Cardstock'}, {'id': 2, 'order_id': 1, 
    #'product_id': 2, 'quantity': 18, 'sub_total_amount': Decimal('3600.00'), 'unit_price': Decimal('200.00'), 'product_name': '40 Pound Letter Stock'}], 'total_amount': Decimal('18900.00')}]
    return render_template("customer/view_orders.html", orders=orders, total_amounts=total_amounts, user=user)
