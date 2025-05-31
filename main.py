from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import string
import random
from cryptography.fernet import Fernet





app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secretkey'
app.permanent_session_lifetime = timedelta(days=5)
csrf = CSRFProtect(app)



  

def generate_password():
    password = random.choices(string.ascii_letters+string.digits+string.punctuation, k=13)
    return "".join(password)


def encrypt_password(password):
    with open("key/key.key", 'r') as f:
        key = f.read()
    fi = Fernet(key)
    cipher_text = fi.encrypt(password)
    return cipher_text

def decrypt_password(cipher_text):
    with open("key/key.key", 'r') as f:
        key = f.read()
    fi = Fernet(key)
    plain_text = fi.decrypt(cipher_text)
    return plain_text.decode('utf-8')


    



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    passwords = db.relationship('Password', backref='owner', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.name
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
with app.app_context():
        db.create_all()  # Create tables


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=5, max=25, message='Username must be in 5 to 25 characters')])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    
class AddPasswordForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=5, max=25, message='Username must be in 5 to 25 characters')])
    password = PasswordField('Password', default="Helloworld")
    email = StringField('Email', validators=[InputRequired()])


    def __repr__(self):
        return f"Name : {self.name}, Password:{self.password}"

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=5, max=25, message='Username must be in 5 to 25 characters')])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    

    def __repr__(self):
        return f"Name : {self.name}, Password:{self.password}"

@app.route("/")
def index():
    if session.permanent == False:
        return redirect(url_for('signin'))
    else:
        return redirect(url_for('home'))

@app.route("/home")
def home():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if not user_id:
        return redirect(url_for('signin'))
    
    password = Password.query.filter_by(user_id=user_id).all() 
    return render_template("home.html", password=password, user=user.username)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddPasswordForm(password="12345")
    
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        user_id = session.get('user_id')
        if not user_id:
            flash("You must be logged in to add a password!", "danger")
            return redirect(url_for('signin'))
        

        print("Name: ",name, "password: ", password, "email: ", email)
        add_password = Password(name=name, password=encrypt_password(password.encode("utf-8")), email=email, user_id=user_id)
        db.session.add(add_password)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form, password=generate_password())

@app.route("/view/<request>", methods=["GET", "POST"])
def view(request):
    password = Password.query.filter_by(id=request, user_id=session.get("user_id")).first_or_404()
    actual_password = decrypt_password(password.password)
    return render_template("view.html", password=password, actual_password=actual_password, )

@app.route("/edit/<response>", methods=["GET", "POST"])
def edit(response):
    form = AddPasswordForm()
    password = Password.query.filter_by(id=response, user_id=session.get("user_id")).first_or_404()
    decrypted_password = decrypt_password(password.password)
    user_id = session.get('user_id')
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        add_password = Password(name=name, password=encrypt_password(password.encode("utf-8")), email=email, user_id=user_id)
        data = Password.query.filter_by(id=response, user_id=session.get("user_id")).first_or_404()
        db.session.delete(data)
        db.session.add(add_password)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", password=password, decrypted_password=decrypted_password, form=form)

@app.route("/delete/<response>", methods=["GET", "POST"])
def delete(response):
    data = Password.query.filter_by(id=response, user_id=session.get("user_id")).first_or_404()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("home"))



@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))
        user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('signin'))
        
    return render_template("register.html", form=form)

@app.route('/signin', methods=["GET", "POST"])    
def signin():
    form =  LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        remember_me = form.remember_me.data
        check_username = User.query.filter_by(username=username).first()
        try:
            check_password = check_password_hash(check_username.password, password)
        except AttributeError as e:
            flash("An error occurred while logging in. Please try again.", "danger")
            print(f"Error: {e}")
            return redirect(url_for('signin'))
        
        

        if  check_username is False:
            print("Could not find username in database")
            return redirect(url_for('signin'))
        if check_password is False:
            flash("Invalid username or password!", "danger")
        if remember_me == True:
            session.permanent = True
            session['username'] = username
            session['user_id'] = check_username.id
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login successful!", "success")
            session['user_id'] = check_username.id
            return redirect(url_for('home'))
        

        
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out!", "success")
    session.permanent = False
    return redirect(url_for('signin'))
    


if __name__ == "__main__":
    app.run(debug=True)
    
