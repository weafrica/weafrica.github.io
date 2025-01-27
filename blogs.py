# Import necessary modules from Flask and SQLite3
from flask import Blueprint, render_template
import sqlite3

# Create a Blueprint for the blogs module
blogs_bp = Blueprint('blogs', __name__)

# Define the path to the database
DATABASE = 'final_project.db'

# Function to get a database connection
def get_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    # Set the row factory to sqlite3.Row to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the list of blogs
@blogs_bp.route('/blogs_list')
def blogs_list():
    # Fetch all blogs from the database
    blogs = get_all_blogs()
    # Render the blogs_list.html template with the blogs
    return render_template('blogs_list.html', blogs=blogs)

# Function to fetch all blogs from the database
def get_all_blogs():
    # Get a database connection
    db = get_db()
    # Create a cursor object
    cursor = db.cursor()
    # Execute the SQL query to select all blogs
    cursor.execute("SELECT * FROM blogs")
    # Fetch all rows from the executed query
    blogs = cursor.fetchall()
    return blogs

@blogs_bp.route('/blog_detail/<int:blog_id>')
def blog_detail(blog_id):
    # Fetch the blog from the database
    blog = blogs.get_blog(blog_id)
    return render_template('blog_detail.html', blog=blog)