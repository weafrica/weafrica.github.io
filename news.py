import sqlite3
from flask import g, Blueprint, render_template, request, redirect, url_for, session, flash
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
        with news_bp.open_resource('schema.sql', mode='r') as f:
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
    # Implement the logic to fetch the article from the database
    pass

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

@news_bp.route('/news_list')
def news_list():
    # Fetch all news articles from the database
    articles = get_all_articles()
    return render_template('news_list.html', articles=articles)

@news_bp.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        body = request.form['body']
        image = request.files['image']
        author = session.get('username')  # Get the author from the session
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(news_bp.root_path, 'static/uploads', filename))
        else:
            filename = None
        
        # Add the news article to the database
        save_article(title, description, body, filename, author)
        return redirect(url_for('news.news_list'))
    return render_template('add_news.html')

@news_bp.route('/news_detail/<int:news_id>')
def news_detail(news_id):
    # Fetch the news article from the database
    article = get_article(news_id)
    return render_template('news_detail.html', article=article)