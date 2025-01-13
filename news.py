import sqlite3
from flask import g

DATABASE = 'final_project.db'

def get_db():
    conn = sqlite3.connect('final_project.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def save_article(title, description, body, image_filename, author):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO articles (title, description, body, image, author) VALUES (?, ?, ?, ?, ?)",
        (title, description, body, image_filename, author)
    )
    db.commit()
    db.close()

def get_all_articles():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT title, description, body, image, author FROM articles")
    articles = cursor.fetchall()
    db.close()
    return articles

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()