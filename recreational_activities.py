# Import necessary modules from Flask and SQLite3
from flask import Blueprint, render_template
import sqlite3

# Create a Blueprint for the recreational activities module
recreational_activities_bp = Blueprint('recreational_activities', __name__)

# Define the path to the database
DATABASE = 'final_project.db'

# Function to get a database connection
def get_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    # Set the row factory to sqlite3.Row to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the list of recreational activities
@recreational_activities_bp.route('/recreational_activities_list')
def recreational_activities_list():
    # Fetch all recreational activities from the database
    activities = get_all_activities()
    # Render the recreational_activities_list.html template with the activities
    return render_template('recreational_activities_list.html', activities=activities)

# Function to fetch all recreational activities from the database
def get_all_activities():
    # Get a database connection
    db = get_db()
    # Create a cursor object
    cursor = db.cursor()
    # Execute the SQL query to select all activities
    cursor.execute("SELECT * FROM activities")
    # Fetch all rows from the executed query
    activities = cursor.fetchall()
    return activities