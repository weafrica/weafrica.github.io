# Import necessary modules from Flask and SQLite3
from flask import Blueprint, render_template, request, redirect, url_for, session, Flask
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
    product = get_product(shop_id)
    return render_template('shop_detail.html', product=product)

# Function to fetch a single product by ID from the database
def get_product(shop_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (shop_id,))
    product = cursor.fetchone()
    return product

# Route to display the add product form
@shop_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    # Check if the user is logged in and the username is 'saulesto'
    if 'username' in session and session['username'] == 'saulesto':
        if request.method == 'POST':
            # Get form data
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image_url = request.form['image_url']  # Added image_url field
            
            # Insert the new product into the database
            insert_product(name, description, price, image_url)
            
            # Redirect to the shop list page
            return redirect(url_for('shop.shop_list'))
        
        # Render the add_product.html template
        return render_template('add_product.html')
    else:
        # Redirect to the shop list page if the user is not 'saulesto'
        return redirect(url_for('shop.shop_list'))

# Function to insert a new product into the database
def insert_product(name, description, price, image_url):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)",
                   (name, description, price, image_url))
    db.commit()

app = Flask(__name__)

# Sample product data
products = [
    {
        'name': 'Product 1',
        'description': 'Description of product 1.',
        'price': 19.99,
        'image_url': 'static/uploads/Angry_bird.jpg'
    },
    {
        'name': 'Product 2',
        'description': 'Description of product 2.',
        'price': 29.99,
        'image_url': 'static/uploads/Angry_bird.jpg'
    },
    {
        'name': 'Product 3',
        'description': 'Description of product 3.',
        'price': 39.99,
        'image_url': 'static/uploads/Angry_bird.jpg'
    }
]

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

@app.route('/shop_list')
def shop_list():
    return render_template('shop_list.html', products=products)

@app.route('/printing')
def printing():
    # Fetch all products from the database
    products = get_all_products()
    # Render the printing.html template with the products
    return render_template('printing.html', products=products)

# Register the Blueprint with the Flask app
app.register_blueprint(shop_bp)

if __name__ == '__main__':
    app.run(debug=True)