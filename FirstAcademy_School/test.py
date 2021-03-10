from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
import uuid
from datetime import datetime
now = datetime.now()
id = uuid.uuid1()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///First_Academy.sqlite3'
db = SQLAlchemy(app)

app.secret_key="4322"

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



@app.route('/blog_display')
def blog_display():
    result1=tbl_blog.query.all()
    # bpdb.set_trace()
    return render_template('blog_display.html',result=result1 )    


# @app.route('/edit_profile/<email>')
# def edit_profile(email):
#     result1=tbl_register.query.filter_by(email=email).first()

    
#     return render_template('edit_profile.html',result=result1 )    




@app.route('/index')
def index():
    # bpdb.set_trace()
    return render_template('index.html')

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
    # bpdb.set_trace()
    
    if request.method == 'POST':
        register = tbl_register(email=request.form['email'],name=request.form['name'],age= request.form['age'],address=request.form['address'], contact_no=request.form['contact_no'],password=request.form['password'],usertype=request.form['usertype'],status="pending",image=request.form['image'])
        db.session.add(register)
        db.session.commit()
        # flash('Record was successfully added')
        return redirect(url_for('show_all'))
    else:   
        return render_template('login.html') 


@app.route('/add_blog/<email>',methods=["GET","POST"])
def add_blog(email):
    # bpdb.set_trace()
    
    if request.method == 'POST':
        
        blog = tbl_blog(bid=id.hex,bdate=now,email=request.form['email'],name=request.form['name'],title= request.form['title'],image=request.form['image'], content=request.form['content'],blogtype=request.form['blogtype'])
        db.session.add(blog)
        db.session.commit()
        email1=request.form['email']
        return redirect(url_for('blog_display',email=email1))
    result1=tbl_register.query.filter_by(email=email).first()   
    return render_template('add_blog.html',result=result1) 

# @app.route('/add_blog/<username>',methods=["GET","POST"])
# def add_blog(username):
#     # bpdb.set_trace()
    
#     if request.method == 'POST':
#         blog = Blog(username=request.form['username'],name=request.form['name'],title= request.form['title'],image=request.form['image'], des=request.form['des'])
#         db.session.add(blog)
#         db.session.commit()
#         return redirect(url_for('blog'))
#     result1=Register.query.filter_by(username=username).first()
#     return render_template('addblog.html',result=result1)








@app.route('/blogs')
def blogs():
    return render_template('/blog.html')    
@app.route('/logout')
def logout():
    
    # bpdb.set_trace()
    session.pop('username', None)
    return redirect(url_for('log')) 


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)

