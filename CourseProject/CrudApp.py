from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "aez2Caipootohd2ahph1zie5aefoh0"
db = SQLAlchemy(app)

class Greeting(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	greeting = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)

GreetingForm = model_form(Greeting, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()

	greeting = Greeting(greeting="Kato terve!", name="Pulkkinen")
	db.session.add(greeting)

	greeting = Greeting(greeting="No terve", name="Sauli")
	db.session.add(greeting)
	db.session.commit()

@app.route("/")
def index():
	greetings = Greeting.query.all()
	return render_template("index.html", greetings=greetings)

@app.route("/<int:id>/delete")
def deleteGreeting(id):
	greeting = Greeting.query.get_or_404(id)
	db.session.delete(greeting)
	db.session.commit()

	flash("Greeting deleted")
	return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/form-page", methods=["GET", "POST"])
def addForm(id=None):
	greeting = Greeting()
	if id:
		greeting = Greeting.query.get_or_404(id)
	
		

	form = GreetingForm(obj=greeting)

	if form.validate_on_submit():
		
		form.populate_obj(greeting)
		
		db.session.add(greeting)
		db.session.commit()

		print("added greeting")
		flash("Added")
		return redirect("/")		

	return render_template("form-page.html", form=form)

if __name__ == "__main__":
	app.run()
