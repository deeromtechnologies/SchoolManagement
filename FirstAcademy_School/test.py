from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
import uuid
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField,IntegerField, PasswordField, validators,ValidationError
from flask_mail import Mail, Message

now = datetime.now()
id = uuid.uuid1()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///First_Academy.sqlite3'
db = SQLAlchemy(app)

mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abcd@gmail.com'
app.config['MAIL_PASSWORD'] = '********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key="4322"



class MyForm(FlaskForm):
    email = StringField('Email Address',validators=[DataRequired(),validators.Length(min=6, max=35)])
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age',validators=[DataRequired()])
    address = StringField('address',validators=[DataRequired()])
    contact_no = StringField('contact_no',validators=[DataRequired(),validators.Length(10)])
    password = PasswordField('password',validators=[DataRequired(),validators.EqualTo('password1', message='Passwords must match')])
    password1 = PasswordField('Repeat Password')
    image = StringField('image', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])

class Blogedit(FlaskForm):
   
    email = StringField('email', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    title= StringField('title', validators=[DataRequired()])
    image= StringField('image', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])    
# bpdb.set_trace() 
class tbl_register(db.Model):

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

# bpdb.set_trace() 
class tbl_blog(db.Model):
    bid= db.Column(db.String(120), primary_key=True)
    bdate = db.Column(db.DateTime, nullable=False)
    email= db.Column(db.String(120), db.ForeignKey('tbl_register'))
    name= db.Column(db.String(120), unique=False, nullable=False)
    title = db.Column(db.String(220), unique=False, nullable=False)
    image = db.Column(db.String(220), unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=False)
    blogtype= db.Column(db.String(80), unique=False, nullable=False)
   
    def __init__(self,bid,bdate,email,name,title,image,content,blogtype):
        self.bid = bid
        self.bdate = bdate
        self.email = email
        self.name = name
        self.title = title
        self.image = image
        self.content = content
        self.blogtype = blogtype



@app.route('/show_all')


def show_all():
    result1=tbl_register.query.all()
    # bpdb.set_trace()
    return render_template('show_all.html',result=result1 )

@app.route('/detail_page/<email>')
def detail_page(email):
    result1=tbl_register.query.filter_by(email=email).first()

    
    return render_template('detail_page.html',result=result1 )



@app.route('/blog_display/<email>')
def blog_display(email):
    # result1=tbl_blog.query.all()
    result1=tbl_blog.query.filter_by(email=email).first()
    # bpdb.set_trace()
    return render_template('blog_display.html',user=result1 )    
    

# @app.route('/edit_profile/<email>')
# def edit_profile(email):
#     result1=tbl_register.query.filter_by(email=email).first()

    
#     return render_template('edit_profile.html',result=result1 )    




@app.route('/index')
def index():
    # bpdb.set_trace()
    return render_template('index.html')



# @app.route('/index2',methods=["POST","GET"])
# def index2():
#     form=MyForm()
#     # bpdb.set_trace()
#     if form.validate_on_submit():
#         return redirect('/success')
#     return render_template('index2.html',form=form)




@app.route('/log',methods=["POST","GET"])
def log():
    if request.method =="POST":
        email=request.form["email"]
        password=request.form["password"]
        # bpdb.set_trace()
        session["email"]=email
        session["password"]=password
        return redirect(url_for('add_blog',email=email))
    else:
        return render_template('log.html')

@app.route('/signup',methods=["POST","GET"])
def signup():
    form=MyForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        register = tbl_register(email=form.email.data,name=form.name.data,age=form.age.data,address=form.address.data,contact_no=form.contact_no.data,password=form.password.data,usertype=request.form['usertype'],status="pending",image=form.image.data)
        db.session.add(register)
        db.session.commit()
        msg = Message('Hello User..You registration completed successfully', sender = 'abcd@gmail.com', recipients = [form.email.data])
        msg.body = "Thank you for registering with us "
        mail.send(msg)
        # return "Sent"
        return redirect(url_for('show_all'))
    else:   
        return render_template('login.html',form=form) 


    


@app.route('/add_blog/<email>',methods=["GET","POST"])
def add_blog(email):
    # bpdb.set_trace()
    form=MyForm(request.form)
    if request.method == 'POST':
        blog = tbl_blog(bid=id.hex,bdate=now,email=request.form['email'],name=request.form['name'],title= form.title.data,image=form.image.data, content=form.content.data,blogtype=request.form['blogtype'])
        db.session.add(blog)
        db.session.commit()
        email1=request.form['email']
        return redirect(url_for('blog_display',email=email1))
    result1=tbl_register.query.filter_by(email=email).first()   
    return render_template('add_blog.html',result=result1,form=form) 



@app.route('/blogs')
def blogs():
    return render_template('/blog.html')    
@app.route('/logout')
def logout():
    
    # bpdb.set_trace()
    session.pop('email', None)
    return redirect(url_for('log')) 



@app.route('/edit/<email>',methods = ['GET','POST'])
def edit(email):
    form = Blogedit(request.form)
    bedit= tbl_blog.query.filter_by(email=email).first()
    if request.method == 'POST':
        if bedit:
            db.session.delete(bedit)
            db.session.commit()
            bedit = tbl_blog(bid=id.hex,bdate=now,email=form.email.data,name=form.name.data,title= form.title.data,image=form.image.data, content=form.content.data,blogtype=request.form['blogtype'])
            db.session.add(bedit)
            db.session.commit()
            email=form.email.data
            # return render_template('blog_display.html',user=email)
            return "You are successfully updated the blog"
        return f"Blog with email = {email} Does not exist"
    result1=tbl_blog.query.filter_by(email=email).first()
    return render_template('edit.html', result=result1,form=form)



if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)

