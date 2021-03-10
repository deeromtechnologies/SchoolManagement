from flask import render_template,Flask,request,url_for,session,redirect

app=Flask("__name__")

@app.route('/home/')
@app.route('/home/<name>')
def home(name=None):
    return render_template('index.html', name=name)
@app.route('/home/about.html')
def about(name=None):
    return render_template('about.html', name=name)
@app.route('/home/gallery.html')
def gallery(name=None):
    return render_template('gallery.html', name=name)

@app.route('/home/blog.html')
def blog(name=None):
    return render_template('blog.html', name=name)
@app.route('/home/staff.html')
def staff(name=None):
    return render_template('staff.html', name=name)
@app.route('/home/contact.html')
def contact(name=None):
    return render_template('contact.html', name=name)
@app.route('/home/404.html')
def pnf(name=None):
    return render_template('404.html', name=name)
@app.route('/home/500.html')
def server(name=None):
    return render_template('500.html', name=name)
@app.route('/home/sitemap.html')
def map(name=None):
    return render_template('sitemap.html', name=name)    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =="POST":

        username=request.form['username']
        # password=request.form['password']
        session["username"]=username
        # if username =="admin" and password=="admin":
        return redirect(url_for('username',username=username))
    else:
        
        if "username" in session:
            return redirect(url_for('username')) 

        return render_template("login.html")



@app.route("/username")
def username():
    if "username" in session:
        username=session["username"]
        return f"<h1>{username}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))    
                                 