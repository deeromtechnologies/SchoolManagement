import os
from sqla_wrapper import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))  # this connects to a database either on Heroku or on localhost




class tbl_register(UserMixin,db.Model):
	 email= db.Column(db.String(120), primary_key=True)
    name= db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(220), unique=False, nullable=False)
    contact_no = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    usertype = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(80), unique=False, nullable=False) 
    image = db.Column(db.String(220), unique=False, nullable=False)
    def __init__(self,email,name,password,usertype,status,age,address,contact_no,image):

		 self.email = email
        self.name = name
        self.age = age
        self.address = address
        self.contact_no = contact_no
        self.password = password
        self.usertype = usertype
        self.status = status
        self.image = image
