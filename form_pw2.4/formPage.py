from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def showForm():
	return render_template('form1.html')

if __name__ == "__main__":
	app.run()
