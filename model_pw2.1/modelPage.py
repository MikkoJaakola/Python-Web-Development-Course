from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
	string = 'world'
	return render_template('base.html', string = string)

if __name__ == '__main__':
	app.run()
