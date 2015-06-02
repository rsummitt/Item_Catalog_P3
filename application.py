from database_setup import Base, Category, Item
from flask import Flask, render_template, request, redirect, jsonify, url_for, session, g
from functools import wraps
from requests_oauthlib import OAuth2Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Github Auth information
client_id = "46a8d3ab8c19a99a4ba4"
client_secret = "49db7ea877757d64bab66bb632422bbdf20b7c0f"
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@app.context_processor
def utility_processor():
    def number_of_items(category_id):
        """Utility Method to get number of items in a particular category"""
        return db_session.query(Item).filter_by(category_id=category_id).count()
    return dict(number_of_items=number_of_items)


@app.before_request
def get_user_info():
    """Gets user information for display if authenticated"""
    if 'oauth_state' in session and 'oauth_token' in session and 'user' not in g:
        github = OAuth2Session(client_id, token=session['oauth_token'])
        g.user = github.get('https://api.github.com/user').json()


def login_required(f):
    """Decorator to apply to methods that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'oauth_state' not in session or 'oauth_token' not in session:
            session['next_uri'] = request.path
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login/')
def login():
    """Redirects user to Github for authorization"""
    github = OAuth2Session(client_id=client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/logout/')
def logout():
    """Removes tokens from user and logs them out"""
    oauth_token = session['oauth_token']
    access_token = oauth_token['access_token']
    github = OAuth2Session(client_id, token=session['oauth_token'])
    url = 'https://api.github.com/applications/%s/tokens/%s' % (client_id, access_token)
    github.delete(url, auth=(client_id, client_secret))
    del g.user
    del session['oauth_state']
    del session['oauth_token']

    return redirect(url_for('get_catalog'))


@app.route('/github-callback')
def github_callback():
    """Callback method that github uses"""
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    session['oauth_token'] = token
    if 'next_uri' in session:
        uri = session['next_uri']
        del session['next_uri']
        return redirect(uri, code=302)
    else:
        return redirect(url_for('get_catalog'))


@app.route('/')
@app.route('/catalog/')
def get_catalog():
    """Displays all categories"""
    categories = db_session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/catalog/category/add/', methods=['GET', 'POST'])
@login_required
def add_category():
    """Displays add category page or commits a new addition"""
    if request.method == 'POST':
        if request.form['name']:
            category = Category(name=request.form['name'])
            db_session.add(category)
            db_session.commit()
            return redirect(url_for('get_catalog'))
    else:
        return render_template('add_category.html')


@app.route('/catalog/category/<int:category_id>/delete/')
@login_required
def delete_category(category_id):
    """Deletes a category"""
    category = db_session.query(Category).filter_by(id=category_id).one()
    db_session.delete(category)
    db_session.commit()
    return redirect(url_for('get_catalog'))


@app.route('/catalog/category/<int:category_id>/items/')
def get_category_items(category_id):
    """Gets items from a specific category"""
    category = db_session.query(Category).filter_by(id=category_id).one()
    category_items = db_session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category_items.html', category=category, category_items=category_items)


@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/')
def get_item(category_id, item_id):
    """Gets a specific items information"""
    category = db_session.query(Category).filter_by(id=category_id).one()
    item = db_session.query(Item).filter_by(category_id=category.id, id=item_id).one()
    return render_template('item.html', category=category, item=item)


@app.route('/catalog/item/add/', methods=['GET', 'POST'])
@login_required
def add_item():
    """Displays an add item page or adds a new item"""
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category']:
            category = db_session.query(Category).filter_by(id=request.form['category']).one()
            item = Item(name=request.form['name'], description=request.form['description'], category_id=category.id)
            db_session.add(item)
            db_session.commit()
            return redirect(url_for('get_item', category_id=category.id, item_id=item.id))
    else:
        categories = db_session.query(Category).all()
        return render_template('add_item.html', categories=categories)


@app.route('/catalog/item/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Displays the edit item page or edits an item"""
    item = db_session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category']:
            category = db_session.query(Category).filter_by(id=request.form['category']).one()
            item.name = request.form['name']
            item.description = request.form['description']
            item.category_id = category.id
            db_session.commit()
            return redirect(url_for('get_item', category_id=category.id, item_id=item.id))
    else:
        categories = db_session.query(Category).all()
        item_category = db_session.query(Category).filter_by(id=item.category_id).one()
        return render_template('edit_item.html', categories=categories, item_category=item_category, item=item)


@app.route('/catalog/item/<int:item_id>/delete/')
@login_required
def delete_item(item_id):
    """Deletes an item"""
    item = db_session.query(Item).filter_by(id=item_id).one()
    category_id = item.category_id
    db_session.delete(item)
    db_session.commit()
    return redirect(url_for('get_category_items', category_id=category_id))


@app.route('/api/catalog')
def categories_json():
    """Returns a json representation of the item catalog"""
    categories = db_session.query(Category).all()
    results = []
    for c in categories:
        result = {'id': c.id, 'name': c.name, 'Items': []}
        for i in db_session.query(Item).filter_by(category_id=c.id):
            result['Items'].append(i.serialize)
        results.append(result)
    return jsonify(Categories=results)


if __name__ == '__main__':
    # This is set to allow testing on HTTP
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.debug = True
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8080)
