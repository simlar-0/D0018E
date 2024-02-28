"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g, request, flash, redirect, url_for, session
from flaskr.auth import login_required
from flaskr.db.store import get_order_orderlines, get_customer_orders
from flaskr.db.user import get_user_password, set_user_password, set_user_details, get_user_by_email
from flaskr.store import get_order_total_amount
import bcrypt


bp = Blueprint("customer", __name__, url_prefix="/user")


@bp.route("/")
@login_required
def profile():
    return render_template("customer/profile.html")

@bp.route("/edit-profile")
@login_required
def view_edit_profile():
    user = g.user
    return render_template("customer/edit_profile.html", user=user)

@bp.route("/edit-profile", methods=["POST"])
@login_required
def edit_profile():
    user = g.user
    forms = request.form.to_dict()
    pass_from_db = get_user_password('Customer', user['id'])
        
    if forms['email'] != user['email']:
        compare_user = get_user_by_email('Customer', forms['email'])
        if compare_user is not None:
            flash("There is already a user with that email address!")
            return redirect(url_for('customer.view_edit_profile'))

    if bcrypt.checkpw(bytes(forms['current_password'], 'utf-8'),bytes(pass_from_db.decode(), 'utf-8')):
        if forms['new_password']:
            hashed_pass = bcrypt.hashpw(bytes(forms['new_password'], 'utf-8'), bcrypt.gensalt())
            set_user_password('Customer', user['id'], hashed_pass)
            
        set_user_details(forms, user['id'])
        # Update session user
        user = get_user_by_email('Customer', forms['email']) 
        session['user_id'] = user
        session.modified = True
        flash("Edit profile successful!")
        return redirect(url_for('customer.profile'))
    flash("Wrong password!")
    return redirect(url_for('customer.view_edit_profile'))

@bp.route("/orders")
@login_required
def view_orders():
    user = g.user
    customer_orders    = get_customer_orders(g.user['id'], with_cart=False)

    if customer_orders:
        order_items = [get_order_orderlines(order['id']) for order in customer_orders]
        total_amounts = [get_order_total_amount(order_item) for order_item in order_items]
        orders = [{'order': order_item, 'total_amount': total_amount, 'order_date': customer_order['order_date'], 'order_status': customer_order['order_status']} for order_item, total_amount, customer_order in zip(order_items, total_amounts, customer_orders)]
        return render_template("customer/view_orders.html", orders=orders, user=user)
    return render_template("customer/view_orders.html", user=user)