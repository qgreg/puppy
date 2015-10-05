from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from puppy import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Shelter, Puppy, Adopter, Adoption, Mailing, PuppyProfile

from puppyPopulator import puppyPopulate

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
	return render_template('index.html')


@app.route('/puppy/')
def puppyList():
    puppy = session.query(Puppy).all()
    profile = session.query(PuppyProfile).all()
    return render_template('puppylist.html', puppy = puppy, profile = profile)


@app.route('/populate/', methods=['GET','POST'])
def puppyPopulator():
	if request.method == 'POST':
		puppyPopulate()
		flash("Puppies have been populated.")
		return redirect(url_for('puppiesHome'))
	else:
		return render_template('populate.html')


@app.route('/puppy/one/<int:puppy_id>/')
def puppyOne(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    #profile = session.query(PuppyProfile).filter_by(puppy_id=puppy_id).one()
    return render_template('puppyone.html', pup = puppy)


@app.route('/puppy/add/', methods=['GET','POST'])
def puppyAdd():
	if request.method == 'POST':
		formDate = datetime.strptime(request.form['dateOfBirth'],'%Y-%m-%d')
		print formDate
		newItem = Puppy(name = request.form['name'], 
			dateOfBirth = formDate,
			breed = request.form['breed'], gender = request.form['gender'],
			weight = request.form['weight'], picture = request.form['picture'])
		session.add(newItem)
		session.commit()
		flash("New puppy has been added.")
		return redirect(url_for('puppyList'))
	else:
		return render_template('puppyadd.html')


@app.route('/puppy/<int:puppy_id>/edit/', methods=['GET','POST'])
def puppyEdit(puppy_id):
	if request.method == 'POST':
		editPuppy = session.query(Puppy).filter_by(id=puppy_id).one()
		editPuppy.name = request.form['name']
		editPuppy.dateOfBirth = datetime.strptime(request.form['dateOfBirth'],'%Y-%m-%d')
		#Handle above ValueErrors
		editPuppy.breed = request.form['breed']
		editPuppy.gender = request.form['gender']
		editPuppy.weight = request.form['weight']
		editPuppy.picture = request.form['picture']
		session.add(editPuppy)
		session.commit()
		flash("Puppy has been edited.")
		return redirect(url_for('puppyOne', puppy_id = puppy_id))
	else:
		editItem = session.query(Puppy).filter_by(id=puppy_id).one()
		return render_template('puppyedit.html', puppy_id=editItem.id, editItem = editItem)


@app.route('/puppy/<int:puppy_id>/delete/', methods=['GET','POST'])
def puppyDelete(puppy_id):
	if request.method == 'POST':
		deletePuppy = session.query(Puppy).filter_by(id=puppy_id).one()
		session.delete(deletePuppy)
		session.commit()
		flash("Puppy has been deleted.")
		return redirect(url_for('puppyList'))
	else:
		deletePuppy = session.query(Puppy).filter_by(id=puppy_id).one()
		return render_template('puppydelete.html', puppy_id = deletePuppy.id, deletePuppy=deletePuppy)

"""
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
