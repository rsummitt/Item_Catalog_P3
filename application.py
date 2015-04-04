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
    return 'Get Catalog'


@app.route('/catalog/<string:category_name>/items')
def get_category_items(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    category_items = session.query(Item).filter_by(category_id=category.id).all()
    return category_items


@app.route('/catalog/<string:category_name>/<string:item_name>')
def get_item(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(category_id=category.id, name=item_name).one()
    return item


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
        return render_template('edit_item.html', item=item)


@app.route('/catalog/<string:item_name>/delete')
def delete_item(item_name):
    return 'Delete Item'


if __name__ == '__main__':
    app.run()
