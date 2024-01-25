import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import sys

from flaskr.db import manipulate_db, query_db

bp = Blueprint("temp_db_test", __name__, url_prefix="/temp_db_test")

@bp.route("/")
def index():
    return render_template("temp_db_test.html")

@bp.route('/abcdef', methods=['POST'])
def button_clicked():
    print('button clicked', file=sys.stderr)
    if request.method == 'POST':
        print('request.method == POST', file=sys.stderr)
        queries = [
            """INSERT INTO flask.Product (ProductID,Name,Description,Price,ImagePath,InStock)
        VALUES (3,'cat','asd',1.0,'asd',1)"""
        ]
        manipulate_db(queries)
        return redirect(url_for("store.index"))
    return redirect(url_for("temp_db_test"))