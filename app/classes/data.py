# This is where all the database collections are defined. A collection is a place to hold a defined 
# set of data like Users, Blogs, Comments. Collections are defined below as classes. Each class name is 
# the name of the data collection and each item is a data 'field' that stores a piece of data.  Data 
# fields have types like IntField, StringField etc.  This uses the Mongoengine Python Library. When 
# you interact with the data you are creating an onject that is an instance of the class.

from sys import getprofile
from tokenize import String
from typing import KeysView
from xmlrpc.client import Boolean

from setuptools import SetuptoolsDeprecationWarning
from app import app
from flask import flash
from flask_login import UserMixin
from mongoengine import FileField, EmailField, StringField, IntField, ReferenceField, DateTimeField, DateField, BooleanField, FloatField, CASCADE
from flask_mongoengine import Document
import datetime as dt
import jwt
from time import time
from bson.objectid import ObjectId

class User(UserMixin, Document):
    createdate = DateTimeField(defaultdefault=dt.datetime.utcnow)
    gid = StringField(sparse=True, unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    gender = StringField()
    image = FileField()
    age = IntField()
    pet = ReferenceField('Pet')
    prononuns = StringField()

    meta = {
        'ordering': ['lname','fname']
    }
    
class Sleep(Document):
    create_date = DateTimeField(defaultdefault=dt.datetime.utcnow)
    day = DateField()
    hours = IntField()
    disturbances = IntField()
    quality = IntField()
    notes = StringField()
    score = IntField()
    modify_date = DateTimeField()
    author = ReferenceField('User',reverse_delete_rule=CASCADE)

    meta = {
        'ordering': ['lname','fname']
    }

class Pet(Document):
    createdate = DateTimeField(defaultdefault=dt.datetime.utcnow)
    author  = ReferenceField('User',reverse_delete_rule=CASCADE) 
    name = StringField()
    type = StringField()
    modify_date = DateTimeField()
    meta = {
        'ordering': ['lname','fname']
    }
