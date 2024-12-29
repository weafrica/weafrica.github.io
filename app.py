from flask import Flask, render_template, request, redirect, url_for, session, g  # Importing necessary modules from Flask
from datetime import timedelta  # Importing timedelta for session lifetime management
from flask_mail import Mail, Message  # Importing Mail and Message for email functionality
import sqlite3  # Importing sqlite3 for database operations
from werkzeug.exceptions import HTTPException
from news import init_db, fetch_and_store_news, schedule_news_fetching





# Initialize Flask application
app = Flask(__name__)

# Secret key for session management (should be kept secret in a real application)
app.secret_key = 'your_secret_key'


@app.errorhandler(500)
def internal_error(error):
    return render_template('apology.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('apology.html'), 404


# Set session lifetime to 7 days
app.permanent_session_lifetime = timedelta(days=7)

# Database file path
DATABASE = 'website.db'

# Function to get a database connection
def get_db():
    # Check if there's already a database connection for the current context
    db = getattr(g, '_database', None)
    if db is None:
        # If not, create a new connection
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This allows us to access columns by name
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
    result = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in rv]
    return (result[0] if result else None) if one else result

# Function to initialize the database with the required tables
def init_db():
    with app.app_context():
        db = get_db()
        db.cursor().executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL
        );
        ''')
        db.commit()

# Initialize the database
init_db()



# Error Handlers
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return render_template('apology.html', error_message=e.description), e.code

@app.errorhandler(500)
def internal_error(error):
    return render_template('apology.html', error_message="Internal Server Error"), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('apology.html', error_message="Page Not Found"), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # Handle non-HTTP exceptions only
    return render_template('apology.html', error_message=str(e)), 500






# Home route
@app.route('/')
def home():
    # Retrieve the username from the session
    username = session.get('user', 'Guest')
    # Render the home.html template with the username
    return render_template('home.html', username=username)

# Shop route
@app.route('/shop')
def shop():
    # Render the shop.html template
    return render_template('shop.html')

# Extra Curricular Activities route
@app.route('/activities')
def activities():
    # Render the activities.html template
    return render_template('activities.html')

# Games route
@app.route('/games')
def games():
    # Render the games.html template
    return render_template('games.html')

# Data Analyzer route
@app.route('/data_analyzer')
def data_analyzer():
    # Query the database for all data
    data = query_db('SELECT * FROM data')
    # Calculate the total, count, and average of the data values
    total = sum(item['value'] for item in data)
    count = len(data)
    average = total / count if count != 0 else 0
    # Render the data_analyzer.html template with the calculated data
    return render_template('data_analyzer.html', data=data, average=average)





# Initialize the database and fetch news
DATABASE = 'news.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This allows us to access columns by name
    return db

@app.route('/news')
def news():
    db = get_db()
    news_articles = db.execute('SELECT title, description, url FROM news').fetchall()
    return render_template('news.html', news_articles=news_articles)





# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Query the database for the user with the provided username and password
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user:
            # Store the username in the session and redirect to the home page
            session['user'] = username
            return redirect(url_for('home'))
    # Render the login.html template
    return render_template('login.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        cellphone = request.form['cellphone']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        if password != confirm_password:
            return render_template('apology.html', error_message="Passwords do not match"), 400
        existing_user = query_db('SELECT * FROM users WHERE username = ? OR email = ?', [username, email], one=True)
        if not existing_user:
            get_db().execute('INSERT INTO users (username, password, email, cellphone, security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?)', [username, password, email, cellphone, security_question, security_answer])
            get_db().commit()
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('apology.html', error_message="Username or Email already exists"), 400
    return render_template('register.html')




# Change Password route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = session.get('user')
        if not username:
            # If the user is not logged in, redirect to the login page
            return redirect(url_for('login'))
        new_password = request.form['new_password']
        # Update the user's password in the database
        get_db().execute('UPDATE users SET password = ? WHERE username = ?', [new_password, username])
        get_db().commit()
        return redirect(url_for('home'))
    # Render the change_password.html template
    return render_template('change_password.html')

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    # Remove the user from the session and redirect to the home page
    session.pop('user', None)
    return redirect(url_for('home'))

# Forgot Password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        # Query the database for the user with the provided username
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user:
            # Redirect to security question page with the user's ID
            return redirect(url_for('security_question', user_id=user['id']))
    # Render the forgot_password.html template
    return render_template('forgot_password.html')

# Security Question route
@app.route('/security_question/<int:user_id>', methods=['GET', 'POST'])
def security_question(user_id):
    if request.method == 'POST':
        answer = request.form['answer']
        # Query the database for the user with the provided answer
        user = query_db('SELECT * FROM users WHERE id = ? AND security_answer = ?', [user_id, answer], one=True)
        if user:
            # Redirect to reset password page with the user's ID
            return redirect(url_for('reset_password', user_id=user_id))
    # Fetch the security question for the user
    user = query_db('SELECT security_question FROM users WHERE id = ?', [user_id], one=True)
    return render_template('security_question.html', user_id=user_id, question=user['security_question'])

# Reset Password route
@app.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Ensure passwords match
        if new_password != confirm_password:
            return "Passwords do not match", 400
        # Update the user's password in the database
        get_db().execute('UPDATE users SET password = ? WHERE id = ?', [new_password, user_id])
        get_db().commit()
        return redirect(url_for('login'))
    # Render the reset_password.html template
    return render_template('reset_password.html', user_id=user_id)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('user')
    if not username:
        return redirect(url_for('login'))
    get_db().execute('DELETE FROM users WHERE username = ?', [username])
    get_db().commit()
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/change_username', methods=['GET', 'POST'])
def change_username():
    if request.method == 'POST':
        username = session.get('user')
        new_username = request.form['new_username']
        if not username:
            return redirect(url_for('login'))
        get_db().execute('UPDATE users SET username = ? WHERE username = ?', [new_username, username])
        get_db().commit()
        session['user'] = new_username
        return redirect(url_for('home'))
    return render_template('change_username.html')

@app.route('/change_cellphone', methods=['GET', 'POST'])
def change_cellphone():
    if request.method == 'POST':
        username = session.get('user')
        new_cellphone = request.form['new_cellphone']
        if not username:
            return redirect(url_for('login'))
        get_db().execute('UPDATE users SET cellphone = ? WHERE username = ?', [new_cellphone, username])
        get_db().commit()
        return redirect(url_for('home'))
    return render_template('change_cellphone.html')

@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if request.method == 'POST':
        username = session.get('user')
        new_email = request.form['new_email']
        if not username:
            return redirect(url_for('login'))
        get_db().execute('UPDATE users SET email = ? WHERE username = ?', [new_email, username])
        get_db().commit()
        return redirect(url_for('home'))
    return render_template('change_email.html')
