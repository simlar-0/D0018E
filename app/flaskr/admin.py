"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g, request, flash, redirect, url_for, session
from flaskr.auth import login_required
from flaskr.db.store import get_order_orderlines, get_customer_orders
from flaskr.db.user import get_user_password, create_user, get_user_by_email, set_user_password, set_user_details, get_all_users
from flaskr.store import get_order_total_amount
import bcrypt


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/customer-list")
def customer_list():
    customers = get_all_users('Customer')
    return render_template("admin/customer_list.html", customers=customers)
