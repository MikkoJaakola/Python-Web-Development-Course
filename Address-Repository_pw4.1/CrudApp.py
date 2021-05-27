from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "aez2Caipootohd2ahph1zie5aefoh0"
db = SQLAlchemy(app)

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	number = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	

ContactForm = model_form(Contact, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()

	contact = Contact(name="Dille", number="05594039", email="Dille.kakelberg@mail.com")
	db.session.add(contact)
	
	contact = Contact(name="Jönssi", number="039382827", email="Jönssi.Kakelberg@mail.com")
	db.session.add(contact)
	
	contact = Contact(name="Hautamäki", number="03930293", email="Hautamäki@mail.com")
	db.session.add(contact)

	
	db.session.commit()

@app.route("/")
def index():
	contacts = Contact.query.all()
	return render_template("index.html", contacts=contacts)

@app.route("/<int:id>/delete")
def deleteContact(id):
	contact = Contact.query.get_or_404(id)
	db.session.delete(contact)
	db.session.commit()

	flash("Contact deleted")
	return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/form-page", methods=["GET", "POST"])
def addForm(id=None):
	contact = Contact()
	if id:
		contact = Contact.query.get_or_404(id)
	
		

	form = ContactForm(obj=contact)

	if form.validate_on_submit():
		
		form.populate_obj(contact)
		
		db.session.add(contact)
		db.session.commit()

		print("added contact")
		flash("Added")
		return redirect("/")		

	return render_template("form-page.html", form=form)

if __name__ == "__main__":
	app.run()
