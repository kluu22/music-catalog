"""
Store standard root for user page navigation
"""

from flask import Blueprint, render_template

# define blueprint for flask application
views = Blueprint('views', __name__)

@views.route('/')
def home():
    # render our home.html in template
    return render_template("home.html")

