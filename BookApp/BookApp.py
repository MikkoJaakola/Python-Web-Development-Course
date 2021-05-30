from flask import Flask, render_template, flash, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "aez2Caipootohd2ahph1zie5aefoh0"
db = SQLAlchemy(app)

from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	book = db.Column(db.String, nullable=False)
	plot = db.Column(db.Text, nullable=False)
	
BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session)

def LoginRequired():
	if not currentUser():
		abort(403)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	passwordHash = db.Column(db.String, nullable=False)

	def setPassword(self, password):
		self.passwordHash = generate_password_hash(password)

	def checkPassword(self, password):
		return check_password_hash(self.passwordHash, password)
		
class UserForm(FlaskForm):
	email = StringField("email", validators=[validators.Email()])
	password = PasswordField("password", validators=[validators.InputRequired()])
	
def currentUser():
	try:
		uid = int(session["uid"])
	except:
		return None
	return User.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser

@app.route("/user/login", methods=["GET", "POST"])
def loginView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data

		password = form.password.data


		user = User.query.filter_by(email=email).first()
		if not user:
			flash("Login failed.")
			print("User not found")
			return redirect("/user/login")
		if not user.checkPassword(password):
			flash("Login failed.")
			print("Wrong password")
			return redirect("/user/login")

		session["uid"] = user.id

		flash("Logged in.")
		return redirect("/")
		
	return render_template("login.html", form=form)
	
@app.route("/user/register", methods=["GET", "POST"])
def registerView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data

		password = form.password.data


		if User.query.filter_by(email=email).first():
			flash("Just login, you have been already registered")
			return redirect("/user/login")

		user = User(email=email)
		user.setPassword(password)

		db.session.add(user)
		db.session.commit()

		flash("You have been registered, please login")
		return redirect("/user/login")

	return render_template("register.html", form=form)
	
	
@app.route("/user/logout")
def logoutView():
	session["uid"] = None
	flash("Signed out")
	return redirect("/")

@app.before_first_request
def initMe():
	db.create_all()

	book = Book(book="Saulin kirja", plot="Ovessa on ainakin miehen mentävä reikä")
	db.session.add(book)

	book = Book(book="Dillen Aspen", plot="Dillen Aspen kolaroidaan kun Bromann töhöilee ratissa")
	db.session.add(book)
	db.session.commit()

@app.route("/")
def index():
	books = Book.query.all()
	return render_template("index.html", books=books)

@app.route("/<int:id>/delete")
def deleteBook(id):
	LoginRequired()
	book = Book.query.get_or_404(id)
	db.session.delete(book)
	db.session.commit()

	flash("Book deleted")
	return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/form-page", methods=["GET", "POST"])
def addForm(id=None):
	LoginRequired()
	book = Book()
	if id:
		book = Book.query.get_or_404(id)
	
		

	form = BookForm(obj=book)

	if form.validate_on_submit():
		
		form.populate_obj(book)
		
		db.session.add(book)
		db.session.commit()

		print("added Kirja")
		flash("Added")
		return redirect("/")		

	return render_template("form-page.html", form=form)

if __name__ == "__main__":
	app.run()
