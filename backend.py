import sqlite3
from flask import Flask, render_template, send_file, request, redirect, url_for, session
import bcrypt


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
		password = temp[2].encode('utf-8')
		#hashed_pwd = bcrypt.checkpw(passwd, password)

		level = temp[3]
		place = temp[4]
		passwd = passwd.encode('utf-8')
		print(passwd)
		print(password)
		if name == username and bcrypt.checkpw(passwd, password):
				verify = 1
	except:
		return 0
	if verify == 1:
		return (name, password, level, place)
	else:
		return 0
############

data = ''
places = ['Manial', 'Gezera', 'Tamooh']
app = Flask(__name__)
app.secret_key = 'hehe'

@app.route('/')
def index():
	return redirect(url_for('login'))


@app.route('/logout')
def logout():
	session.pop('logged', None)
	session.pop('level', None)
	session.pop('name', None)
	return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		passwd = request.form['password']
		data = auth(username, passwd)
		if data:
			session['level'] = data[2]
			session['place'] = data[3]
			session['logged'] = 1
			session['name'] = data[0]

			#print(data[2], "hello")
			return redirect(url_for('main'))
		else:
			return 'wrong'
	return send_file('templates/login.html')

@app.route('/main')
def main():
	if session.get('logged') == 1:
		lev = session.get('level')
		print(session.get('name'))
		return render_template("main.html")
	else:
		return redirect(url_for('login'))


@app.route("/remove", methods=['POST', 'GET'])
def remove():
	shop_name = ''
	if session.get('logged') == 1:
		if request.method == 'POST':
			#print(request.form)
			quantity = request.form['quantity']
			item = request.form['item']
			shop = session.get('place')
			print("remove these ", quantity, item, shop)
			response = "Input Accepted"
			response += """
			<script>
	        	setTimeout(function() {
	            window.location.href = "/remove";
	        	}, 1000);  // Redirect back to the previous page after 2 seconds
    		</script>
    		"""
			return response
		else:
			lev = session.get('level')
		place = session.get('place')
		if place == 0:
			return render_template('remove_manager.html')
		elif place == 1:
			shop_name = "Manial"
			
		elif place == 2:
			shop_name = "Gezera"

		elif place == 3:
			shop_name = "Tamooh"
		session['place'] = place
		return render_template('remove.html', shop=shop_name)
	else:
		return redirect(url_for('login'))

@app.route('/remove_manager', methods=['POST', 'GET'])
def remove_manager():
	if session.get('level') != 1:
		return redirect(url_for('remove'))

	if session.get('logged') == 1:
		if request.method == 'POST':
			quantity = request.form['quantity']
			item = request.form['item']
			shop = request.form['shop']
			print("remove these ", quantity, item, shop)
			response = "Input Accepted"
			response += """
			<script>
	        	setTimeout(function() {
	            window.location.href = "/remove_manager";
	        	}, 1000);  // Redirect back to the previous page after 2 seconds
    		</script>
    		"""
			return response
		else:
			lev = session.get('level')
		return render_template('remove_manager.html')
	else:
		return redirect(url_for('login'))


@app.route('/add_manager', methods=['POST', 'GET'])
def add_manager():
	if session.get('level') != 1:
		return redirect(url_for('add'))

	if session.get('logged') == 1:
		if request.method == 'POST':
			#print(request.form)
			#print("yess")
			quantity = request.form['quantity']
			item = request.form['item']
			shop = request.form['shop']
			print("add these ", quantity, item, shop)
			response = "Input Accepted"
			response += """
			<script>
	        	setTimeout(function() {
	            window.location.href = "/add_manager";
	        	}, 1000);  // Redirect back to the previous page after 2 seconds
    		</script>
    		"""
			return response
		else:
			lev = session.get('level')
		return render_template('add_manager.html')
	else:
		return redirect(url_for('login'))


@app.route('/add', methods=['POST', 'GET'])
def add():
	shop_name = ''
	if session.get('logged') == 1:
		if request.method == 'POST':
			#print(request.form)
			quantity = request.form['quantity']
			item = request.form['item']
			shop = session.get('place')
			print("add these ", quantity, item, shop)
			response = "Input Accepted"
			response += """
			<script>
	        	setTimeout(function() {
	            window.location.href = "/add";
	        	}, 1000);  // Redirect back to the previous page after 2 seconds
    		</script>
    		"""
			return response
		else:
			lev = session.get('level')
		place = session.get('place')
		if place == 0:
			print("yes")
			return render_template('add_manager.html')
		elif place == 1:
			shop_name = "Manial"

		elif place == 2:
			shop_name = "Gezera"

		elif place == 3:
			shop_name = "Tamooh"
		session['place'] = place
		return render_template('add.html', shop=shop_name)
		
	else:
		return redirect(url_for('login'))

@app.route('/generate', methods=['POST', 'GET'])
def generate():
	if session.get('level') == 1:
		if request.method == 'POST':
			choice = request.form['option']
			session['target'] = choice
			print(choice, "pressed")
			if choice == "manial":
				table_name = "alum_manial"
			elif choice == "gezera":
				table_name = "alum_gezera"
			elif choice == "tamooh":
				table_name = "alum_tamooh"

			con = sqlite3.connect('inventory.db')
			curs = con.cursor()
			curs.execute("select * from %s;"%(table_name))
			data = curs.fetchall()
			con.close()
			return render_template("generate.html", data=data)
		else:
			return render_template('generate.html', data='')
	elif session.get('level') == 2:
		if session.get('place') == 1:
			table_name = "alum_manial"
		elif session.get('place') == 2:
			table_name = "alum_gezera"
		elif session.get('place') == 3:
			table_name = "alum_tamooh"
		con = sqlite3.connect('inventory.db')
		curs = con.cursor()
		curs.execute("select * from %s;"%(table_name))
		data = curs.fetchall()
		con.close()
		return render_template("generateL.html", data=data, name=places[session.get('place')-1])
	else:
		return "You are not authorized"

app.run(port=80, host='192.168.1.57')


