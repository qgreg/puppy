from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def puppyPicFix():
	
	puppy_images = ["https://mykennel.org/Uploads/dogImage/Poodle%20Pup%203.jpg",\
		"http://assets.nydailynews.com/polopoly_fs/1.1245686!/img/httpImage/image.jpg_gen/derivatives/article_970/afp-cute-puppy.jpg",\
		"https://s-media-cache-ak0.pinimg.com/236x/df/89/9f/df899f55b5f2eddea78b2c29881c043a.jpg",\
		"http://media1.s-nbcnews.com/ij.aspx?404;http://sys03-media.s-nbcnews.com:80/j/streams/2012/December/121204/1C5045406-tdy-121204-puppy-names-02.blocks_desktop_large.jpg",\
		"https://s-media-cache-ak0.pinimg.com/236x/33/d2/e0/33d2e069ac4f57fdf4869b35e72e016b.jpg"]
	puppy = session.query(Puppy).all()

	for i in puppy:
		editPuppy = session.query(Puppy).filter_by(id=i.id).one()
		editPuppy.picture = random.choice(puppy_images)
		session.add(editPuppy)
		session.commit()

