"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g, request, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flaskr.db.store import (
    get_order_orderlines, 
    get_customer_orders, 
    get_all_products, 
    get_one_product, 
    update_product, 
    add_product as db_add_product, 
    get_non_cart_orderlines,
    get_non_cart_statuses,
    change_order_status
    )
from flaskr.db.user import (
    get_all_users,
    get_user_by_id,
    delete_user,
    set_user_details,
    get_user_by_email,
    set_user_password,
    )
from flaskr.store import get_order_total_amount
from flaskr.auth import manager, admin
from pathlib import Path
import bcrypt


bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@bp.route("/manage_orders")
@manager
def manage_orders():
    orderlines = get_non_cart_orderlines()
    orders = {}
    for orderline in orderlines:
        if orderline['order_id'] not in orders.keys():
            orders[orderline['order_id']] = {
                'customer_id':orderline['customer_id'],
                'order_date':orderline['order_date'],
                'order_status_id':orderline['order_status_id'],
                'status':orderline['status'],
                'customer_name':orderline['customer_name'],
                'total':int(orderline['sub_total_amount'])
            }
        else:
            orders[orderline['order_id']]['total'] += orderline['sub_total_amount']

    order_statuses = get_non_cart_statuses()
    return render_template("admin/manage_orders.html", orders=orders.items(), statuses = order_statuses)

@bp.route("/manage_orders?<int:order_id>", methods=["POST"])
@manager
def change_status(order_id):
    forms = request.form.to_dict()
    if 'change_status' not in forms.keys():
        return redirect(url_for('admin.manage_orders'))
    new_status = forms['change_status']
    statuses = get_non_cart_statuses()
    for status in statuses:
        if status['name']==new_status:
            change_order_status(order_id, status['id'])
            break
    return redirect(url_for('admin.manage_orders'))

@bp.route("/manage-products")
@manager
def product_list():
    products = get_all_products(include_unlisted=True)
    return render_template("admin/product_list.html", products=products)

@bp.route("/manage-products/product-id=<int:id>")
@manager
def product_details(id):
    product = get_one_product(id)
    return render_template("admin/edit_product.html", product=product)

@bp.route("/manage-products/edit_product", methods=['GET', 'POST'])
@manager
def edit_product():
    upload_image(request)
    forms = request.form.to_dict()
    
    file = request.files['file']
    if file.filename == '':
        forms['image_path'] = request.form['old_image_path']
    else:
        image_path = Path('/images') / request.files['file'].filename
        forms['image_path'] = str(image_path.as_posix())
    
    update_product(forms)
    flash('Product details edited successfully')
    return redirect(url_for('admin.product_list'))   

def upload_image(request):
    
    if 'file' not in request.files:
        return False
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(Path(current_app.config['UPLOAD_FOLDER'], filename))
        return True
    return False
    
@bp.route("/manage-products/add_product", methods=['GET', 'POST'])
@manager
def add_product():
    if request.method == 'POST':
        upload_image(request)
        
        forms = request.form.to_dict()
        image_path = Path('/images') / request.files['file'].filename
        forms['image_path'] = str(image_path.as_posix())
        db_add_product(forms)
        return redirect(url_for('admin.product_list'))
    return render_template("admin/add_product.html")

@bp.route("/customer/<int:id>/edit-profile")
@admin
def view_edit_profile(id):
    user = get_user_by_id(id, 'Customer')
    return render_template("admin/edit_customer_profile.html", user=user)

@bp.route("/customer/<int:id>/edit-profile", methods=["POST"])
@admin
def edit_profile(id):
    user = get_user_by_id(id, 'Customer')
    forms = request.form.to_dict()
        
    if forms['email'] != user['email']:
        compare_user = get_user_by_email('Customer', forms['email'])
        if compare_user is not None:
            flash("There is already a user with that email address!")
            return redirect(url_for('admin.view_edit_profile', id=id))

    if forms['new_password']:
        hashed_pass = bcrypt.hashpw(bytes(forms['new_password'], 'utf-8'), bcrypt.gensalt())
        set_user_password('Customer', user['id'], hashed_pass)
            
    set_user_details(forms, user['id'])
    flash("Edit profile successful!")
    return redirect(url_for('admin.view_edit_profile', id=id))

@bp.route("/customer/<int:id>/delete")
@admin
def delete_customer(id):
    """
    Delete a customer from the database.

    :returns A redirect to the customer list.
    """
    delete_user(id, 'Customer')
    return redirect(url_for('admin.customer_list'))

