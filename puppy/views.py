from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from puppy import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import PUPPY_POST_PER_PAGE, SHELTER_POST_PER_PAGE

from models import Base, Shelter, Puppy, Adopter, Adoption, Mailing, PuppyProfile

from puppyPopulator import puppyPopulate
from pagination import Pagination
from puppyimagefixer import puppyPicFix

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
In your Python code, you should add methods for performing all 
of the database functionalities described below:

All CRUD operations on 
X	Puppies, 
	Shelters, 
	and Owners
Switching or Balancing Shelter Population and Protecting 
	against overflows
Viewing a Puppy Profile
Adopting a New Puppy
X Creating and Styling Templates (optionally with Bootstrap)
X Adding Flash Messages
X BONUS: Pagination
"""


@app.route('/')
@app.route('/home/')
def puppiesHome():
	return render_template('index.html')


@app.route('/puppy/')
@app.route('/puppy/<int:page>/')
def puppyList(page=1):
	count = session.query(Puppy).count()
	offset = (page - 1) * PUPPY_POST_PER_PAGE
	puppy = session.query(Puppy).order_by(Puppy.id).slice(offset, offset + PUPPY_POST_PER_PAGE)
	paginate = Pagination(page, PUPPY_POST_PER_PAGE, count)
	profile = session.query(PuppyProfile).all()
	print "Count ", count, "Offset ", offset, "Page ", page, \
		"Limit ", PUPPY_POST_PER_PAGE, "Pages ", paginate.pages
	return render_template('puppylist.html', puppy = puppy, profile = profile, page = page, paginate = paginate)


@app.route('/puppy/one/<int:puppy_id>/')
def puppyOne(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    #profile = session.query(PuppyProfile).filter_by(puppy_id=puppy_id).one()
    return render_template('puppyone.html', pup = puppy)


@app.route('/puppy/add/', methods=['GET','POST'])
def puppyAdd():
	if request.method == 'POST':
		formDate = datetime.strptime(request.form['dateOfBirth'],'%Y-%m-%d')
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


@app.route('/shelter/')
@app.route('/shelter/<int:page>/')
def shelterList(page=1):
	count = session.query(Shelter).count()
	offset = (page - 1) * SHELTER_POST_PER_PAGE
	shelter = session.query(Shelter).order_by(Shelter.id).slice(offset, offset + SHELTER_POST_PER_PAGE)
	paginate = Pagination(page, SHELTER_POST_PER_PAGE, count)
	print "Count ", count, "Offset ", offset, "Page ", page, \
		"Limit ", SHELTER_POST_PER_PAGE, "Pages ", paginate.pages
	return render_template('shelterlist.html', shelter = shelter, page = page, paginate = paginate)


@app.route('/shelter/one/<int:shelter_id>/')
def shelterOne(shelter_id):
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    return render_template('shelterone.html', shelter = shelter)


@app.route('/shelter/add/', methods=['GET','POST'])
def shelterAdd():
	if request.method == 'POST':		
		newItem = Shelter(name = request.form['name'])
		newItem.address = request.form['address']
		newItem.city = request.form['city']
		newItem.state = request.form['state']
		newItem.zipCode = request.form['zipCode']
		newItem.email = request.form['email']
		newItem.website = request.form['website']
		newItem.current_capacity = request.form['current_capacity']
		newItem.max_capacity = request.form['max_capacity']
		session.add(newItem)
		session.commit()
		flash("New shelter has been added.")
		return redirect(url_for('shelterList'))
	else:
		return render_template('shelteradd.html')


@app.route('/shelter/<int:shelter_id>/edit/', methods=['GET','POST'])
def shelterEdit(shelter_id):
	if request.method == 'POST':
		editShelter = session.query(Shelter).filter_by(id=shelter_id).one()
		editShelter.name = request.form['name']
		editShelter.address = request.form['address']
		editShelter.city = request.form['city']
		editShelter.state = request.form['state']
		editShelter.zipCode = request.form['zipCode']
		editShelter.email = request.form['email']
		editShelter.website = request.form['website']
		editShelter.current_capacity = request.form['current_capacity']
		editShelter.max_capacity = request.form['max_capacity']
		session.add(editShelter)
		session.commit()
		flash("shelter has been edited.")
		return redirect(url_for('shelterOne', shelter_id = shelter_id))
	else:
		editItem = session.query(Shelter).filter_by(id=shelter_id).one()
		return render_template('shelteredit.html', shelter_id=editItem.id, editItem = editItem)


@app.route('/shelter/<int:shelter_id>/delete/', methods=['GET','POST'])
def shelterDelete(shelter_id):
	if request.method == 'POST':
		deleteShelter = session.query(Shelter).filter_by(id=shelter_id).one()
		session.delete(deleteShelter)
		session.commit()
		flash("Shelter has been deleted.")
		return redirect(url_for('shelterList'))
	else:
		deleteShelter = session.query(Shelter).filter_by(id=shelter_id).one()
		return render_template('shelterdelete.html', shelter_id = deleteShelter.id, \
			deleteShelter=deleteShelter)

@app.route('/populate/', methods=['GET','POST'])
def puppyPopulator():
	if request.method == 'POST':
		puppyPopulate()
		flash("Puppies have been populated.")
		return redirect(url_for('puppiesHome'))
	else:
		return render_template('populate.html')


@app.route('/picfix/', methods=['GET','POST'])
def puppyPicFixer():
	if request.method == 'POST':
		puppyPicFix()
		flash("Puppies images have been replaced.")
		return redirect(url_for('puppyList'))
	else:
		return render_template('picfix.html')


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
