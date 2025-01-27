# Import necessary modules from Flask and SQLite3
from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

# Create a Blueprint for the shop module
shop_bp = Blueprint('shop', __name__)

# Define the path to the database
DATABASE = 'final_project.db'

# Function to get a database connection
def get_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    # Set the row factory to sqlite3.Row to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the list of products
@shop_bp.route('/shop_list')
def shop_list():
    # Fetch all products from the database
    products = get_all_products()
    # Render the shop_list.html template with the products
    return render_template('shop_list.html', products=products)

# Function to fetch all products from the database
def get_all_products():
    # Get a database connection
    db = get_db()
    # Create a cursor object
    cursor = db.cursor()
    # Execute the SQL query to select all products
    cursor.execute("SELECT * FROM products")
    # Fetch all rows from the executed query
    products = cursor.fetchall()
    return products

@shop_bp.route('/shop_detail/<int:shop_id>')
def shop_detail(shop_id):
    # Fetch the product from the database
    product = shop.get_product(shop_id)
    return render_template('shop_detail.html', product=product)