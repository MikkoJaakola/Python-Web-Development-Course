from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form



app = Flask(__name__)
app.secret_key = "shougephipooboh2ahM4oa0zashi3x"
db = SQLAlchemy(app)

class Greeting(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	greeting = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)
	
GreetingForm = model_form(Greeting, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()

	greeting = Greeting(greeting="Kato terve", name="Pulkkinen")
	db.session.add(greeting)

	greeting = Greeting(greeting="No terve", name="Sauli")
	db.session.add(greeting)
	db.session.commit()

@app.route("/")
def index():
	greetings = Greeting.query.all()
	return render_template("index.html", greetings=greetings)

@app.route("/Form-Page", methods=["GET", "POST"])
def addForm():
	form = GreetingForm()
	return render_template("form-page.html", form=form)

if __name__ == "__main__":
	app.run()
