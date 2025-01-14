from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import shop  # Import the shop module

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop_list():
    # Fetch all products from the database
    products = shop.get_all_products()
    return render_template('shop_list.html', products=products)

@shop_bp.route('/shop_detail/<int:shop_id>')
def shop_detail(shop_id):
    # Fetch the product from the database
    product = shop.get_product(shop_id)
    return render_template('shop_detail.html', product=product)