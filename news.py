import sqlite3
from flask import g, Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, abort
from functools import wraps
import os
from werkzeug.utils import secure_filename

news_bp = Blueprint('news', __name__)

DATABASE = 'final_project.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with news_bp.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_article(title, description, body, filename, author):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO articles (title, description, body, image, author) VALUES (?, ?, ?, ?, ?)",
        (title, description, body, filename, author)
    )
    db.commit()

def get_article(news_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (news_id,))
    return cursor.fetchone()

def get_all_articles():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, description, body, image, author FROM articles")
    articles = cursor.fetchall()
    if articles is None:
        return []
    return articles

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Function to handle the news list page
@news_bp.route('/news_list')
def news_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    return render_template('news_list.html', articles=articles, user_is_on_news_list_page=True)

# Function to handle adding a news article
@news_bp.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == 'POST':
        # Get the form data
        title = request.form['title']
        description = request.form['description']
        body = request.form['body']
        image = request.files['image']  # Get the image file from the form
        author = session.get('username')  # Get the author from the session
        
        # Check if the image file is allowed and save it
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(news_bp.root_path, 'static/uploads', filename))
        else:
            filename = None
        
        # Add the news article to the database
        save_article(title, description, body, filename, author)
        # Redirect to the news list page after saving the article
        return redirect(url_for('news.news_list'))
    
    # Render the add news template if the request method is GET
    return render_template('add_news.html')

# Function to handle displaying the details of a news article
@news_bp.route('/news_detail/<int:news_id>')
def news_detail(news_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (news_id,))
    news_article = cursor.fetchone()
    if news_article is None:
        abort(404)
    return render_template('news_detail.html', news_article=news_article)

# Function to handle searching for news articles
@news_bp.route('/search')
def search():
    query = request.args.get('query')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM articles WHERE title LIKE ? OR description LIKE ? OR body LIKE ?", 
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    return render_template('search_results.html', results=results)

@news_bp.route('/search_autocomplete')
def search_autocomplete():
    query = request.args.get('query')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title FROM articles WHERE title LIKE ? OR description LIKE ? OR body LIKE ?", 
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    return jsonify(results=[dict(row) for row in results])
