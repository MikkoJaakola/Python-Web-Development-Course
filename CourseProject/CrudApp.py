from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "aez2Caipootohd2ahph1zie5aefoh0"
db = SQLAlchemy(app)

class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	lyrics = db.Column(db.Text, nullable=False)
	name = db.Column(db.String, nullable=False)

SongForm = model_form(Song, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()

	song = Song(lyrics="Kato terve!", name="Pulkkinen")
	db.session.add(song)

	song = Song(lyrics="No terve", name="Sauli")
	db.session.add(song)
	db.session.commit()

@app.route("/")
def index():
	songs = Song.query.all()
	return render_template("index.html", songs=songs)

@app.route("/<int:id>/delete")
def deleteSong(id):
	song = Song.query.get_or_404(id)
	db.session.delete(song)
	db.session.commit()

	flash("Song deleted")
	return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/form-page", methods=["GET", "POST"])
def addForm(id=None):
	song = Song()
	if id:
		song = Song.query.get_or_404(id)
	
		

	form = SongForm(obj=song)

	if form.validate_on_submit():
		
		form.populate_obj(song)
		
		db.session.add(song)
		db.session.commit()

		print("added song")
		flash("Added")
		return redirect("/")		

	return render_template("form-page.html", form=form)

if __name__ == "__main__":
	app.run()
