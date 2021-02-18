import sqlite3
import csv

conn = sqlite3.connect('main.db')

def create_db():
	c = conn.cursor()
	# Create table
	c.execute('''CREATE TABLE matches
				(status text, date text, team text, final_score text, first_half text)''')
	conn.commit()
	conn.close()

def insert_db():
	c = conn.cursor()
	# insert a row of data
	with open('items.csv','r') as fin:
		dr = csv.DictReader(fin)
		to_db = [(i['status'], i['date'], i['team'], i['final_score'], i['first_half']) for i in dr]
	c.executemany("INSERT INTO matches (status, date, team, final_score, first_half) VALUES (?, ?, ?, ?, ?)", to_db)
	
	conn.commit()
	conn.close()
