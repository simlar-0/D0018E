"""
Flask blueprint for logged in Customer views.
"""
from flask import Blueprint, render_template, g, request, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flaskr.db.store import get_order_orderlines, get_customer_orders, get_all_products, get_one_product, update_product, remove_product as db_remove_product
from flaskr.db.user import get_all_users, get_user_by_id
from flaskr.store import get_order_total_amount
from flaskr.auth import manager
from pathlib import Path


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
    customer_orders = get_customer_orders(id)
    user = get_user_by_id(id, 'Customer')
    if customer_orders:
        order_items = [get_order_orderlines(order['id']) for order in customer_orders]
        total_amounts = [get_order_total_amount(order_item) for order_item in order_items]
        orders = [{'order': order_item, 'total_amount': total_amount, 'order_date': customer_order['order_date'], 'order_status': customer_order['order_status']} for order_item, total_amount, customer_order in zip(order_items, total_amounts, customer_orders)]
        return render_template("admin/view_customer_orders.html", orders=orders, user=user)
    return render_template("admin/view_customer_orders.html", user=user)

@bp.route("/manage-products")
@manager
def product_list():
    products = get_all_products()
    return render_template("admin/product_list.html", products=products)

@bp.route("/manage-products/product-id=<int:id>")
@manager
def product_details(id):
    product = get_one_product(id)
    return render_template("admin/product_details.html", product=product)

@bp.route("/manage-products/edit_product", methods=['GET', 'POST'])
def edit_product():
    forms = request.form.to_dict()
    upload_image(request)
    
    image_path = Path('/images') / request.files['file'].filename
    forms['image_path'] = str(image_path.as_posix())
    update_product(forms)
    return redirect(url_for('admin.product_list'))
    
    
def upload_image(request):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(Path(current_app.config['UPLOAD_FOLDER'], filename))
        flash('Product details edited successfully')
        return redirect(request.url)
    return None

@bp.route("/manage-products/remove_product/product-id=<int:id>")
def remove_product(id):
    db_remove_product(id)
    redirect(url_for('admin.product_list'))