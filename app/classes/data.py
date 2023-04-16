
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
    pet_type = ReferenceField('Pet')
    userID = IntField
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
    sleep_score = IntField()
    author = ReferenceField('User',reverse_delete_rule=CASCADE)

    meta = {
        'ordering': ['lname','fname']
    }

class Pet(Document):
    createdate = DateTimeField(defaultdefault=dt.datetime.utcnow)
    author  = ReferenceField('User',reverse_delete_rule=CASCADE) 
    name = StringField()
    pettag = StringField()
    pet_type = StringField()
    modify_date = DateTimeField()
    
    health = IntField()

    meta = {
        'ordering': ['lname','fname']
    }

class Column(Document):
    col1=IntField
    col2=IntField
    col3=IntField
    col4=IntField
    col5=IntField
    col6=IntField
    col7=IntField
