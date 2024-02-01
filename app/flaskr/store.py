"""
Flask blueprint for browsing items.
"""
from flask import Blueprint
from flask import render_template
from flask import request

from flaskr.db import  get_some_products, count_products


bp = Blueprint("store", __name__)
LIMIT = 12 #TODO: move magic constants somewhere else

@bp.route("/")
def index():
    try:
        page = int(request.args.get('page', 1))
        page = page if page > 0 else 1
    except TypeError:
        page = 1
    except ValueError:
        page = 1
    products = get_some_products(LIMIT, (page-1)*LIMIT)
    total_product_count = count_products()
    return render_template("store/index.html", products=products, page=page, limit=LIMIT, tot_prod=total_product_count)

@bp.route("/cart")
def cart():
    return render_template("store/cart.html")

@bp.route("/product")
def product():
    return render_template("store/product.html")