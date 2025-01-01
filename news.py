import sqlite3
from flask import g

DATABASE = 'final_project.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_article(title, description, body, image_url, author):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO articles (title, description, body, image_url, author) VALUES (?, ?, ?, ?, ?)",
        (title, description, body, image_url, author)
    )
    db.commit()

def get_all_articles():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT title, description, body, image_url FROM articles")
    articles = cursor.fetchall()
    return articles

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()