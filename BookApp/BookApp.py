from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "aez2Caipootohd2ahph1zie5aefoh0"
db = SQLAlchemy(app)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	book = db.Column(db.String, nullable=False)
	plot = db.Column(db.Text, nullable=False)
	
BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session)

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
	book = Book.query.get_or_404(id)
	db.session.delete(book)
	db.session.commit()

	flash("Book deleted")
	return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/form-page", methods=["GET", "POST"])
def addForm(id=None):
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
