from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
	bands = ['Slayer', 'Testament', 'Megadeth', 'Pantera']
	return render_template('base.html',  bands = bands)

if __name__ == '__main__':
	app.run()
