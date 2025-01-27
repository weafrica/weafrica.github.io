# Import necessary modules from Flask and SQLite3
from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

# Create a Blueprint for the data analyzer module
data_analyzer_bp = Blueprint('data_analyzer', __name__)

# Define the path to the database
DATABASE = 'final_project.db'

# Function to get a database connection
def get_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    # Set the row factory to sqlite3.Row to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the list of data analyzers
@data_analyzer_bp.route('/data_analyzer_list')
def data_analyzer_list():
    # Fetch all data analyzers from the database
    analyzers = get_all_analyzers()
    # Render the data_analyzer_list.html template with the analyzers
    return render_template('data_analyzer_list.html', analyzers=analyzers)

# Function to fetch all data analyzers from the database
def get_all_analyzers():
    # Get a database connection
    db = get_db()
    # Create a cursor object
    cursor = db.cursor()
    # Execute the SQL query to select all analyzers
    cursor.execute("SELECT * FROM analyzers")
    # Fetch all rows from the executed query
    analyzers = cursor.fetchall()
    return analyzers

# Route to display the details of a specific data analyzer
@data_analyzer_bp.route('/data_analyzer_detail/<int:analyzer_id>')
def data_analyzer_detail(analyzer_id):
    # Fetch the data analyzer from the database using the analyzer_id
    analyzer = get_analyzer(analyzer_id)
    # Render the data_analyzer_detail.html template with the analyzer
    return render_template('data_analyzer_detail.html', analyzer=analyzer)

# Function to fetch a specific data analyzer from the database
def get_analyzer(analyzer_id):
    # Get a database connection
    db = get_db()
    # Create a cursor object
    cursor = db.cursor()
    # Execute the SQL query to select the analyzer by id
    cursor.execute("SELECT * FROM analyzers WHERE id = ?", (analyzer_id,))
    # Fetch the row from the executed query
    return cursor.fetchone()