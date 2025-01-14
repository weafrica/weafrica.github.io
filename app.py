from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from datetime import timedelta
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError
import os
from functools import wraps
from news import news_bp  # Import the news blueprint
from shop import shop_bp  # Import the shop blueprint
from data_analyzer import data_analyzer_bp  # Import the data_analyzer blueprint
from game import game_bp  # Import the game blueprint
from recreational_activities import recreational_activities_bp  # Import the recreational_activities blueprint
from blogs import blogs_bp  # Import the blogs blueprint

# Initialize Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Register the blueprints
app.register_blueprint(news_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(data_analyzer_bp)
app.register_blueprint(game_bp)
app.register_blueprint(recreational_activities_bp)
app.register_blueprint(blogs_bp)

# Define the function to check if the profile picture exists
def profile_picture_exists(filename):
    return os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename))

app.jinja_env.globals.update(profile_picture_exists=profile_picture_exists)

# Define the profile endpoint
@app.route('/profile')
def profile():
    # Retrieve the username from the session
    username = session.get('username')
    profile_picture = session.get('profile_picture')
    return render_template('profile.html', username=username, profile_picture=profile_picture)

# Set session lifetime
app.permanent_session_lifetime = timedelta(days=7)

# Database file path
DATABASE = 'final_project.db'

# Upload folder
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads/profile_pictures')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for image upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    # Handle HTTP exceptions
    return render_template('apology.html', error_message=str(e), error_code=e.code), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    # Handle non-HTTP exceptions only
    return render_template('apology.html', error_message=str(e), error_code=500), 500

@app.route('/', endpoint='index')
def index():
    # Retrieve the username from the session
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate the username and password with the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT password, profile_picture FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[0], password):
            session['username'] = username
            session['profile_picture'] = user[1]
            print(f"Session data: {session}")  # Debug print
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'login_error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hash the password and save the user to the database
        hashed_password = generate_password_hash(password, method='sha256')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        flash('Registration successful! Please log in.', 'register_success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        if 'retrieve_question' in request.form:
            username = request.form['username']
            # Retrieve the security question from the database
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT security_question FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user:
                security_question = user[0]
                return render_template('forgot_password.html', username=username, security_question=security_question)
            else:
                flash('Username not found. Please try again.', 'forgot_password_error')
        elif 'reset_password' in request.form:
            username = request.form['username']
            security_answer = request.form['security_answer']
            new_password = request.form['new_password']
            # Retrieve the security answer from the database
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT security_answer FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[0], security_answer):
                # Hash the new password
                hashed_new_password = generate_password_hash(new_password)
                # Update the password in the database
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
                db.commit()
                flash('Password reset successful. Please log in with your new password.', 'forgot_password_success')
                return redirect(url_for('login'))
            else:
                flash('Incorrect security answer. Please try again.', 'forgot_password_error')
    return render_template('forgot_password.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    username = session.get('username')
    # Add logic to delete the account from the database
    return redirect(url_for('index'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        # Add logic to change the password
        return redirect(url_for('settings'))
    return render_template('change_password.html')

@app.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'POST':
        # Add logic to change the username
        return redirect(url_for('settings'))
    return render_template('change_username.html')

@app.route('/change_cellphone', methods=['GET', 'POST'])
@login_required
def change_cellphone():
    if request.method == 'POST':
        # Add logic to change the cellphone number
        return redirect(url_for('settings'))
    return render_template('change_cellphone.html')

@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        # Add logic to change the email
        return redirect(url_for('settings'))
    return render_template('change_email.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))

    # Perform search in different categories
    news_results = news.search_articles(query)
    shop_results = shop.search_products(query)
    data_analyzer_results = data_analyzer.search_data(query)
    game_results = game.search_games(query)
    recreational_activities_results = recreational_activities.search_activities(query)
    blog_results = blogs.search_blogs(query)

    # Combine all results
    results = news_results + shop_results + data_analyzer_results + game_results + recreational_activities_results + blog_results

    return render_template('search_results.html', results=results)

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('No file part')
        return redirect(url_for('profile'))
    file = request.files['profile_picture']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('profile'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session['profile_picture'] = filename
        flash('Profile picture uploaded successfully')
        return redirect(url_for('profile'))
    else:
        flash('File type not allowed')
        return redirect(url_for('profile'))

# Set session lifetime to 7 days
app.permanent_session_lifetime = timedelta(days=7)

if __name__ == '__main__':
    app.run(debug=True)