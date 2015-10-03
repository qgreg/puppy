from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from puppy import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Shelter, Puppy, Adopter, Adoption, Mailing, PuppyProfile

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
In your Python code, you should add methods for performing all 
of the database functionalities described below:

All CRUD operations on Puppies, Shelters, and Owners
Switching or Balancing Shelter Population and Protecting 
	against overflows
Viewing a Puppy Profile
Adopting a New Puppy
Creating and Styling Templates (optionally with Bootstrap)
Adding Flash Messages
BONUS: Pagination
"""


@app.route('/')
@app.route('/home/')
def puppiesHome():
	print "This works, four."
	return render_template('index.html')

"""
@app.route('/puppy/')
def puppyListFull():
    puppy = session.query(Puppy).all()
    return render_template('puppylist.html', puppy = puppy)


@app.route('/puppy/<int:puppy_id>/')
def puppyList(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template('puppylist.html', puppy = puppy)

@app.route('/puppy/add/', methods=['GET','POST'])
def puppyAdd():
	if request.method == 'POST':
		newItem = Puppy(name = request.form['name'])
		session.add(newItem)
		session.commit()
		flash("New puppy has been added.")
		return redirect(url_for('puppiesHome'))
	else:
		return render_template('puppyadd.html')

@app.route('/puppy/<int:puppy_id>/edit/', methods=['GET','POST'])
def puppyEdit(puppy_id):
	if request.method == 'POST':
		editPuppy = session.query(Puppy).filter_by(id=puppy_id).one()
		editPuppy.name = request.form['name']
		session.add(editPuppy)
		session.commit()
		flash("Puppy has been edited.")
		return redirect(url_for('puppyList', puppy_id = puppy_id))
	else:
		editItem = session.query(Puppy).filter_by(id=puppy_id).one()
		return render_template('editpuppy.html', puppy_id=editIt.restaurant_id, menu_id = editItem.id, editedItem = editItem)


@app.route('/puppy/<int:puppy_id>/delete/', methods=['GET','POST'])
def puppyDelete(puppy_id):
	if request.method == 'POST':
		deletePuppy = session.query(Puppy).filter_by(id=puppy_id).one()
		session.delete(deletePuppy)
		session.commit()
		flash("Puppy has been deleted.")
		return redirect(url_for('puppyList', puppy_id=puppy_id))
	else:
		deleteItem = session.query(Puppy).filter_by(id=puppy_id).one()
		return render_template('deletepuppy.html', puppy_id = deletePuppy.id, deleteItem=deletePuppy)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(
		restaurant_id = restaurant.id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(
		id = menu_id).one()
	return jsonify(MenuItems=[item.serialize])
"""

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
