from flask import Flask, render_template, request, redirect, jsonify, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def get_catalog():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/catalog/<int:category_id>/items')
def get_category_items(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    category_items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category_items.html', category=category, category_items=category_items)


# Todo: Refactor this to use an id not a string
@app.route('/catalog/<int:category_id>/<int:item_id>')
def get_item(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(category_id=category.id, item_id=item_id).one()
    return item


# Todo: Refactor this to use an id not a string
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category']:
            item.name = request.form['name']
            item.description = request.form['description']
            item.category = request.form['category']
            return redirect(url_for('get_catalog'))
    else:
        # Todo: Create edit_item.html form
        return render_template('edit_item.html', item=item)


# Todo: Refactor this to use an id not a string
@app.route('/catalog/<string:item_name>/delete')
def delete_item(item_name):
    # Todo: Implement delete item
    return 'Delete Item'


@app.route('/api/catalog.json')
def categories_json():
    categories = session.query(Category).all()
    results = []
    for c in categories:
        result = {'id': c.id, 'name': c.name, 'Items': []}
        for i in session.query(Item).filter_by(category=c):
            result['Items'].append(i.serialize)
        results.append(result)
    return jsonify(Categories=results)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
