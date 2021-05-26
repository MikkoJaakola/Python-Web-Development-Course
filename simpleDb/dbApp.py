from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)

class Greeting(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	greeting = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)

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

if __name__ == "__main__":
	app.run()
