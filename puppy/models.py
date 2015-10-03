import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
   
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    city = Column(String(250))
    state = Column(String(2))
    zipCode = Column(String(10))
    email = Column(String(250))
    website = Column(String(250))
    current_capacity = Column(Integer)
    max_capacity = Column(Integer)
    id = Column(Integer, primary_key=True)


class Puppy(Base):
    __tablename__ = 'puppy'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    dateOfBirth = Column(Date)
    breed = Column(String(250))
    gender = Column(String(250))
    weight = Column(Integer)
    picture = Column(String(250))
    shelter_id = Column(Integer,ForeignKey('shelter.id'))
    shelter = relationship(Shelter) 


class PuppyProfile(Base):
    """Each puppy is allowed one profile which can contain
    a url to the puppy's photo, a description about the puppy,
    and any special needs the puppy may have. Implement this
    table and the foreign key relationship in your code.
    """
    __tablename__ = 'puppyprofile'

    puppy = relationship(Puppy)
    description = Column(String(250))
    special_needs = Column(String(250))
    puppy_id = Column(Integer, ForeignKey('puppy.id'), 
        primary_key = True)
 

class Adoption(Base):
    """Class of adoptions"""
    __tablename__ = 'adoption'

    id = Column(Integer, primary_key = True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    adopter_id = Column(Integer, ForeignKey('adopter.id'))
    date_of_adoption = Column(Date)    


class Adopter(Base):
    """Class of adopters"""
    __tablename__ = 'adopter'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    mailing_id = Column(Integer, ForeignKey('mailing.id'))
    email = Column(String(250))


class Mailing(Base):
    __tablename__ = 'mailing'

    id = Column(Integer, primary_key = True)
    address = Column(String(250))
    city = Column(String(250))
    state = Column(String(2))
    zip = Column(String(10))


def Getter():
    pass


def Setter():
    pass


def PuppyCheckIn():
    pass


def ShelterBalance():
    pass


engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)