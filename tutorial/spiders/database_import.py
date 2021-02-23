import sqlite3
import csv

conn = sqlite3.connect('test.db')

def create_db():
	c = conn.cursor()
	# Create table
	c.execute('''CREATE TABLE matches
				(status text, data text, team_1 text, team_2 text, final_score_home text, final_score_away text, first_half_home text, first_half_away text, win_status text)''')
	conn.commit()

def insert_db():
	c = conn.cursor()
	# insert a row of data
	with open('items.csv','r') as fin:
		dr = csv.DictReader(fin)
		to_db = [(i['status'], i['data'], i['team_1'], i['team_2'], i['final_score_home'], i['final_score_away'], i['first_half_home'], i['first_half_away']) for i in dr]
	c.executemany("INSERT INTO meci (status, data, home_team, away_team, home_Fresult, away_Fresult, home_HTresult, away_HTresult) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", to_db)
	conn.commit()

def define_winner():
    c = conn.cursor()

    c.execute("UPDATE matches SET win_status=CASE WHEN final_score_home>final_score_away THEN '1' WHEN final_score_home<final_score_away THEN '2' WHEN final_score_home=final_score_away THEN 'X' WHEN status LIKE '%Not started%' THEN 'i' END") 
    conn.commit()
    
