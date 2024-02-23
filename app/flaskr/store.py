"""
Flask blueprint for browsing items.
"""
from flask import (
    Blueprint, 
    render_template, 
    request, 
    session, 
    g, 
    flash, 
    redirect, 
    url_for
)
from flaskr.auth import login_required

from flaskr.db.store import(
    get_some_products, 
    count_products, 
    get_one_product, 
    update_cart as update_cart_in_db,
    get_amount_in_cart,
    get_cart_id,
    create_cart,
    get_cart_orderlines,
    checkout as checkout_db,
    get_product_reviews
)


bp = Blueprint("store", __name__)
LIMIT = 12 #TODO: move magic constants somewhere else

@bp.route("/")
def index():
    total_product_count = count_products()  
    try:
        page = int(request.args.get('page', 1))
        page = page if page > 0 else 1
    except TypeError:
        page = 1
    except ValueError:
        page = 1
    except IndexError:
        page = 1
    finally:
        if page > total_product_count//LIMIT + 1:
            page = 1

        
    products = get_some_products(LIMIT, (page-1)*LIMIT)
    
    for product in products:
        reviews = get_product_reviews(product['id'])
        if reviews:
            product['rating'] = get_average_rating(reviews)

    return render_template("store/index.html", products=products, page=page, limit=LIMIT, tot_prod=total_product_count)

@bp.route("/cart")
@login_required
def cart():
    cart_id = get_cart_id(g.user['id'])
    cart    = get_cart_orderlines(g.user['id'])
    total_amount = get_order_total_amount(cart)
    return render_template("store/cart.html", cart=cart, cart_id=cart_id, total_amount=total_amount)

@bp.route("/cart", methods=['POST'])
@login_required
def update_cart():
    product_ids = request.form.getlist('product_id')
    products = []
    quantities = request.form.getlist('quantity')
    
    for product_id in product_ids:
        products.append(get_one_product(product_id))

    update_cart_in_db(g.user['id'], products, quantities)
    
    return redirect(url_for('store.cart'))

@bp.route("/product", methods=["GET"])
def product_info():
    try:
        product_id = int(request.args.get('id', 1))
    except TypeError:
        product_id = 1
    except ValueError:
        product_id = 1

    if g.user is None: # This updates the text below the greyed out "add to cart" button
        flash("You must be logged in to add to cart.")
       
    try:
        product = get_one_product(product_id)
    except IndexError:
        return render_template("store/product.html", id=product_id, product=None)

    reviews = get_product_reviews(product_id)

    if reviews:
        product['rating'] = get_average_rating(reviews)

    if not g.user:
        return render_template("store/product.html", id=product_id, product=product, reviews=reviews, do_not_show_add=True)

    for review in reviews:
        if g.user and review['customer_id'] == g.user['id']:
            return render_template("store/product.html", id=product_id, product=product, reviews=reviews, do_not_show_add=True)     
    return render_template("store/product.html", id=product_id, product=product, reviews=reviews)

@bp.route("/product", methods=["POST"])
@login_required
def add_to_cart():
    try:
        product_id = int(request.args.get('id', 1))
    except TypeError:
        product_id = 1
    except ValueError:
        product_id = 1

    product = get_one_product(product_id)
    quantity = int(request.form.get('quantity'))

    if get_cart_id(g.user['id']) is None:
        create_cart(g.user['id'])

    in_cart_amount = get_amount_in_cart(g.user['id'], product_id)
    update_cart_in_db(g.user['id'], [product], [quantity+in_cart_amount])

    return redirect(url_for('store.product_info', id=product_id))

def get_order_total_amount(order):
    total = 0
    for orderline in order:
        total += orderline['sub_total_amount']
    return total

def get_average_rating(reviews):
    total = 0
    for review in reviews:
        total += review['rating']
    return total / len(reviews)

@bp.route("/order-confirmation")
@login_required
def checkout():
    checkout_db(g.user['id'])
    return render_template("store/checkout.html")