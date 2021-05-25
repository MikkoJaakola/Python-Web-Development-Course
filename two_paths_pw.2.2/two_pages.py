from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def first_page():
	return render_template("firstPage.html")
@app.route("/secondPage")
def second_page():
	return render_template("secondPage.html")

if __name__ == '__main__':
	app.run()
