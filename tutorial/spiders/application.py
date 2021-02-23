from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3,csv

DATABASE='test.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sergiu/bettinganalyzer/tutorial/spiders/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Meci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    home_team = db.Column(db.String(50), nullable=False)
    away_team = db.Column(db.String(50), nullable=False)
    home_Fresult = db.Column(db.Integer(), nullable=True)
    away_Fresult = db.Column(db.Integer(), nullable=True)
    home_HTresult = db.Column(db.Integer(), nullable=True)
    away_HTresult = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return '<Meci %r>' % self.id

    def create(self, status, data, home_team, away_team, home_Fresult, away_Fresult, home_HTresult, away_HTresult):
        self.status = status
        self.data = data
        self.home_team = home_team
        self.away_team = away_team
        self.home_Fresult = home_Fresult
        self.away_Fresult = away_Fresult
        self.home_HTresult = home_HTresult
        self.away_HTresult = away_HTresult
        

@app.route('/')

def get_db():
    db = getattr(app, '_database', None)
    if db is None: 
        db = app._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * from meci")
    rows = cursor.fetchall()

    return render_template('index.html', echipa = rows)

def read_csv():
    meci_nou = Meci()
    with open('items.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            meci_nou.create(row['status'],row['data'],row['team_1'],row['team_2'],row['final_score_home'],row['final_score_away'],row['first_half_home'],row['first_half_away'])
            db.session.add(meci_nou)
            db.session.commit()


@app.route('/test')

def team_form():
    echipa = request.args.get('echipa')
    home = 0;
    away = 0;
    draw = 0;
    db = getattr(app, '_database', None)
    if db is None:
        db = app._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    cursor=db.execute('SELECT * from meci WHERE home_team LIKE "%{val1}%" OR away_team LIKE "%{val1}%" GROUP BY data having status LIKE "%Finished%" ORDER BY data DESC LIMIT 10;'.format(val1=echipa))
    rows = cursor.fetchall()

    return render_template('index.html', homewin = home, awaywin = away, draw = draw, echipa=rows)

@app.route('/calculate')

def calculate():
    db = getattr(app, '_database', None)
    if db is None:
        db = app._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    cursor=db.execute('SELECT  win_status, COUNT(*) FROM(SELECT * from meci WHERE home_team LIKE "%Bologna%" OR away_team LIKE "%Bologna%" ORDER BY status ASC,data DESC LIMIT 10)GROUP BY win_status;')
    row = cursor.fetchall()
    return render_template("calculate.html", stat = row) 

if __name__ == '__main__':
    app.run()
