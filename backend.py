import sqlite3
from flask import Flask, render_template, send_file, request, redirect, url_for, session


lev = 0
################
def auth(username, passwd):
	con = sqlite3.connect('users.db')
	curs = con.cursor()
	name = ''
	password = ''
	level = 0
	verify = 0
	curs.execute("select * from user where name = '%s';" %(username))
	row = curs.fetchall()
	try:
		temp = row[0]
		name = temp[1]
		password = temp[2]
		level = temp[3]
		if name == username and password == passwd:
				verify = 1
	except:
		return 0
	if verify == 1:
		return (name, password, level)
	else:
		return 0
############

data = ''

app = Flask(__name__)
app.secret_key = 'hehe'

@app.route('/')
def index():
	return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	global lev
	if request.method == 'POST':
		username = request.form['username']
		passwd = request.form['password']
		data = auth(username, passwd)
		if data:
			session['level'] = data[2]
			#print(data[2], "hello")
			return redirect(url_for('main'))
		else:
			return 'wrong'
	return send_file('templates/login.html')

@app.route('/main')
def main():
	lev = session.get('level')
	#print(lev)
	return render_template("main.html", level = lev)
	
@app.route('/add')
def add():
	lev = session.get('level')
	return render_template('add.html')

@app.route('/generate')
def gen():
	con = sqlite3.connect('inventory.db')
	curs = con.cursor()
	curs.execute("select * from alum_manial;")
	return curs.fetchall()
app.run(port=80, host='192.168.1.57')

