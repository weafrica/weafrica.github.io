from flask import Flask, render_template, request, redirect, url_for, session, g, send_from_directory
from datetime import timedelta
import sqlite3

# Initialize Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Set session lifetime
app.permanent_session_lifetime = timedelta(days=7)

# Database file path
DATABASE = 'final_project.db'

# Function to get a database connection
def get_db():
    # Check if there's already a database connection for the current context
    db = getattr(g, '_database', None)
    if db is None:
        # If not, create a new connection
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to close the database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to execute a database query and return the results
def query_db(query, args=(), one=False):
    # Execute the query with the given arguments
    cur = get_db().execute(query, args)
    # Fetch all the results
    rv = cur.fetchall()
    cur.close()
    # Return a single result if requested, otherwise return all results
    return (rv[0] if rv else None) if one else rv

# Function to initialize the database with the required tables
def init_db():
    with app.app_context():
        db = get_db()
        db.cursor().executescript('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL
        );
        ''')
        db.commit()

# Initialize the database
init_db()

# Route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# News section route
@app.route('/news')
def news():
    news_articles = query_db('SELECT * FROM news')
    return render_template('news.html', articles=news_articles)

# Blogs section route
@app.route('/blogs')
def blogs():
    blog_posts = query_db('SELECT * FROM blogs')
    return render_template('blogs.html', blogs=blog_posts)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if not existing_user:
            get_db().execute('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
            get_db().commit()
            session['user'] = username
            return redirect(url_for('home'))
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user:
            session['user'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

# User logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Activity listings route
@app.route('/activities')
def activities_view():
    activities_data = query_db('SELECT * FROM activities')
    return render_template('activities.html', activities=activities_data)

# E-commerce route
@app.route('/shop')
def shop():
    return render_template('shop.html')

# Games route
@app.route('/games')
def games_view():
    games_data = query_db('SELECT * FROM games')
    return render_template('games.html', games=games_data)

# Data analyzer route
@app.route('/data_analyzer')
def data_analyzer():
    data = query_db('SELECT * FROM data')
    total = sum(item['value'] for item in data)
    count = len(data)
    average = total / count if count != 0 else 0
    return render_template('data_analyzer.html', data=data, average=average)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
