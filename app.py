from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=7)

# Mock Data
news_articles = [
    {'title': 'News Article 1', 'content': 'Content of news article 1'},
    {'title': 'News Article 2', 'content': 'Content of news article 2'}
]

blog_posts = [
    {'author': 'Alice', 'title': 'Blog Post 1', 'content': 'Content of blog post 1'},
    {'author': 'Bob', 'title': 'Blog Post 2', 'content': 'Content of blog post 2'}
]

activities = [
    {'name': 'Activity 1', 'description': 'Description of activity 1'},
    {'name': 'Activity 2', 'description': 'Description of activity 2'}
]

users = {}

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# News section route
@app.route('/news')
def news():
    return render_template('news.html', articles=news_articles)

# Blogs section route
@app.route('/blogs')
def blogs():
    return render_template('blogs.html', blogs=blog_posts)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            session['user'] = username
            return redirect(url_for('home'))
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

# Activity listings route
@app.route('/activities')
def activities():
    return render_template('activities.html', activities=activities)

# E-commerce route
@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run(debug=True)
