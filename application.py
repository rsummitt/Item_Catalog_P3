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


@app.route('/catalog/<int:category_id>/delete')
def delete_category(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    session.delete(category)
    session.commit()
    return redirect(url_for('get_catalog'))


@app.route('/catalog/<int:category_id>/items')
def get_category_items(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    category_items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category_items.html', category=category, category_items=category_items)


@app.route('/catalog/<int:category_id>/<int:item_id>')
def get_item(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(category_id=category.id, id=item_id).one()
    return render_template('item.html', category=category, item=item)


@app.route('/catalog/item/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category']:
            category = session.query(Category).filter_by(id=request.form['category']).one()
            item = Item(name=request.form['name'], description=request.form['description'], category_id=category.id)
            session.add(item)
            session.commit()
            return redirect(url_for('get_item', category_id=category.id, item_id=item.id))
    else:
        categories = session.query(Category).all()
        return render_template('add_item.html', categories=categories)


@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category']:
            category = session.query(Category).filter_by(id=request.form['category']).one()
            item.name = request.form['name']
            item.description = request.form['description']
            item.category_id = category.id
            session.commit()
            return redirect(url_for('get_item', category_id=category.id, item_id=item.id))
    else:
        categories = session.query(Category).all()
        return render_template('edit_item.html', categories=categories, item=item)


@app.route('/catalog/<int:item_id>/delete')
def delete_item(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    category_id = item.category_id
    session.delete(item)
    session.commit()
    return redirect(url_for('get_category_items', category_id=category_id))


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
