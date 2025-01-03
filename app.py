from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from datetime import timedelta
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError
import os
from functools import wraps
import news

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
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed extensions for image upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Decorator to require login for certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
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
    username = session.get('username', 'Guest')
    # Render the index.html template with the username
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
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        profile_picture = request.files['profile_picture']
        
        # Validate the input
        errors = []
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if not email:
            errors.append("Email is required.")
        if not security_question:
            errors.append("Security question is required.")
        if not security_answer:
            errors.append("Security answer is required.")
        if profile_picture and not profile_picture.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            errors.append("Invalid profile picture format. Only PNG, JPG, JPEG, and GIF are allowed.")
        
        # Check if username or email already exists
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            errors.append("Username or email already exists.")
        
        if errors:
            for error in errors:
                flash(error, 'register_error')
            return render_template('register.html')
        
        # Hash the password and security answer
        hashed_password = generate_password_hash(password)
        hashed_security_answer = generate_password_hash(security_answer)
        
        # Save the profile picture if provided
        profile_picture_filename = None
        if profile_picture:
            profile_picture_filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename))
        
        # Save the user information in the database
        cursor.execute("INSERT INTO users (username, password, email, security_question, security_answer, profile_picture) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, hashed_password, email, security_question, hashed_security_answer, profile_picture_filename))
        db.commit()
        
        flash('Registration successful. Please log in.', 'register_success')
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

@app.route('/news_list')
def news_list():
    # Render the news_list.html template
    return render_template('news_list.html')

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        flash('You need to be logged in to add news.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        body = request.form['body']
        image = request.files['image']
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        # Add logic to save the news article along with the image filename
        # Assuming you have a function to save the article in the database
        news.save_article(title, description, body, filename)
        
        flash('News article added successfully!', 'success')
        return redirect(url_for('news_list'))
    
    return render_template('add_news.html')

@app.route('/shop')
def shop():
    # Render the shop.html template
    return render_template('shop.html')

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

@app.route('/data_analyzer')
def data_analyzer():
    # Render the data_analyzer.html template
    return render_template('data_analyzer.html')

@app.route('/game')
def game():
    # Render the game.html template
    games = [
        {"title": "Game 1", "description": "Description for game 1"},
        {"title": "Game 2", "description": "Description for game 2"}
    ]
    return render_template('game.html', games=games)

@app.route('/recreational_activities')
def recreational_activities():
    # Render the recreational_activities.html template
    return render_template('recreational_activities.html')

@app.route('/blogs')
def blogs():
    # Render the blogs.html template
    return render_template('blogs.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # Add logic to handle the search query
    return render_template('search_results.html', query=query)

# Set session lifetime to 7 days
app.permanent_session_lifetime = timedelta(days=7)

if __name__ == '__main__':
    news.init_db()  # Initialize the database
    app.run(debug=True, port=5001)