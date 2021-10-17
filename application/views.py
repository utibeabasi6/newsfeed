# Import needed modules
from functools import wraps

import hashlib
import requests
from flask import Blueprint, request, redirect, session, render_template, url_for, flash, jsonify

from config import Config
from .database import Database

# Initialize some global variables
apiKey = Config.API_KEY
baseApiUrl = f'http://newsapi.org/v2/top-headlines?country=ng&apiKey={apiKey}'
categoryApiUrl = f'http://newsapi.org/v2/top-headlines?country=ng&apiKey={apiKey}&category='
searchApiUrl = f'https://newsapi.org/v2/everything?apiKey={apiKey}&q='

# Create the views blueprint to handle all our views
views = Blueprint('views', __name__, template_folder='templates', static_folder='static')

# Initialize our database to be used for CRUD operations within the application
db = Database()


# UTILITY FUNCTIONS
def hash_password(password):
    """
    Takes a password and returns a hashed value to be stored in the database
    :param password: string
    :return: string
    """
    hashed = hashlib.sha256(password.encode('utf-8'))
    return hashed.hexdigest()


def login_required(f):
    """
    Decorator to ensure only logged in users have access to certain pages
    :param f: View
    :return: Function
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return f(*args, **kwargs)
        else:
            flash('You must be logged in to view this page', category='warning')
            return redirect(url_for('views.login'))

    return wrap


# Views

@views.route('/')
@views.route('/home/', methods=['GET', 'POST'])
def home():
    """
    Renders the homepage whenever the user enters '/' or '/home/' in the url
    Fetches latest news from the news api and sends it to the template
    :return: Template
    """
    categories = ['Technology', 'Sports', 'Health', 'Science', 'Entertainment', 'Business']
    if request.method == 'POST':
        q = request.form.get('q')
        try:
            response = requests.get(searchApiUrl + q)
            newslist = response.json()['articles']
        except requests.exceptions.ConnectionError:
            flash(f'An error occurred while fetching the news on {q}', category='danger')
            return render_template('search.html', newslist=None, q=q)
        else:
            return render_template('search.html', newslist=newslist, q=q)
    try:
        response = requests.get(baseApiUrl)
        newslist = response.json()['articles']
    except:
        flash('An error occurred while fetching the latest news', category='danger')
        return render_template('home.html', news=None, categories=categories)
    else:
        return render_template('home.html', newslist=newslist, categories=categories)


@views.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Renders the login page when the url path points to '/login/'
    Handles authenticating users and logging them in
    Sets the session name object if it does not exist
    :return: Template
    """
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        if db.check_user(name, hash_password(password)):
            session['name'] = name
            flash('You have been logged in successfully', 'success')
            return redirect(url_for('views.home'))
        flash('Invalid username or password', category='danger')
    elif session.get('name') is not None:
        flash('You have already been logged in!', category='info')
        return redirect(url_for('views.home'))
    return render_template('login.html')


@views.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Renders the registration page for new users to sign up
    Hashes the password to be stored in the database for security
    Redirects to the home page on successful sign up
    Logs new users in automatically
    :return: Template
    """
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        user_added = db.add_user(name, hash_password(
            password))  # Adds the user  to the database and checks if successfully added
        if user_added:
            session['name'] = name
            flash('Registration Successful', category='success')
            return redirect(url_for('views.home'))
        flash('User already exists', category='danger')
    return render_template('register.html')


@views.route('/logout/')
@login_required
def logout():
    """
    Logs the user out by removing the username from the session dict
    :return: Redirect
    """
    if session.get('name'):
        session.pop('name', None)
        flash('You have been logged out successfully', category='success')
        return redirect(url_for('views.home'))


@views.route('/category/<category>/')
@login_required
def category(category):
    """
    Fetches the news based on the requested category
    Displays the category page when the user requests
    :param category: string
    :return: Template
    """
    categories = ['Technology', 'Sports', 'Health', 'Science', 'Entertainment', 'Business']
    if category in categories:
        try:
            response = requests.get(categoryApiUrl + category)
            newslist = response.json()['articles']
            newslist = [{'title': news['title'], 'urlToImage': news['urlToImage'], 'description': news['description'],
                         'publishedAt': news['publishedAt'], 'author': news['author']} for news in newslist]
        except:
            flash('An error occurred while fetching the latest news', category='danger')
            return render_template('category.html', newslist=None, category=category)
        else:
            return render_template('category.html', newslist=newslist, category=category)
    flash('Category does not exist', 'danger')
    return redirect(url_for('views.home'))


@views.route('/api/setHistory/', methods={'POST'})
def setHistory():
    if request.method == 'POST':
        print(request.form.keys())
        return jsonify({'message': 'received'})
