from flask import Flask, render_template
import sqlite3

DATABASE='main.db'

app = Flask(__name__)

@app.route('/')

def get_db():
	db = getattr(app, '_database', None)
	if db is None: 
		db = app._database = sqlite3.connect(DATABASE)
	cursor = db.execute("SELECT * from matches")
	rows = cursor.fetchall()

	return render_template('index.html', object = rows)
	


if __name__ == '__main__':
	app.run()
