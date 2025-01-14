from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import blogs  # Import the blogs module

blogs_bp = Blueprint('blogs', __name__)

@blogs_bp.route('/blogs')
def blogs_list():
    # Fetch all blogs from the database
    all_blogs = blogs.get_all_blogs()
    return render_template('blogs_list.html', blogs=all_blogs)

@blogs_bp.route('/blog_detail/<int:blog_id>')
def blog_detail(blog_id):
    # Fetch the blog from the database
    blog = blogs.get_blog(blog_id)
    return render_template('blog_detail.html', blog=blog)