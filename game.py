# Import necessary modules from Flask and SQLite3
from flask import Blueprint, render_template
import sqlite3

# Create a Blueprint for the game module
game_bp = Blueprint('game', __name__)

# Define the path to the database
DATABASE = 'final_project.db'

# Function to get a database connection
def get_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    # Set the row factory to sqlite3.Row to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the list of games
@game_bp.route('/game_list')
def game_list():
    # Fetch all games from the database
    games = get_all_games()
    # Render the game_list.html template with the games
    return render_template('game_list.html', games=games)

# Function to fetch all games from the database
def get_all_games():
    # Get a database connection
    db = get_db()
    # Create a cursor object
    cursor = db.cursor()
    # Execute the SQL query to select all games
    cursor.execute("SELECT * FROM games")
    # Fetch all rows from the executed query
    games = cursor.fetchall()
    return games

@game_bp.route('/game_detail/<int:game_id>')
def game_detail(game_id):
    # Fetch the game from the database
    game_detail = game.get_game(game_id)
    return render_template('game_detail.html', game=game_detail)