import sqlite3
from flask import Flask, render_template, send_file, request, redirect, url_for, session
import bcrypt
import ssl
import datetime

log = 'log.txt'


lev = 0

def keeplog(data_to_write, name, addr):
	current_time = datetime.datetime.now()
	tempdt = "[%s %s] "%(current_time.strftime("%d/%m/%Y"), current_time.strftime("%H:%M:%S"))
	tempdt += " [%s from %s] " %(name, addr)
	data_to_write = str(tempdt) + "\t%s\n"%(str(data_to_write))
	logfile = open(log, 'w')
	logfile.write(data_to_write)
	logfile.close()


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

		level = temp[3] #1 admin, 2 normal add/remove, 3
		place = temp[4] # 0 admin, 1 manial, 2 gezera, 3 tamooh
		work = temp[5]  #0 admin, 1 alum, 2 acc, 3 fiber
		passwd = passwd.encode('utf-8')
		#print(passwd)
		#print(password)
		if name == username and bcrypt.checkpw(passwd, password):
				verify = 1
	except:
		return 0
	if verify == 1:
		return (name, password, level, place, work)
	else:
		return 0
############

places = ['Manial', 'Gezera', 'Tamooh']
work_type = ['Aluminium', 'Accessories', 'Fiber']
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
	session.pop('place', None)
	session.pop('logged', None)
	keeplog("Logout", session['name'], request.remote_addr)
	return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		passwd = request.form['password']
		data = auth(username, passwd)
		if data:
			keeplog("new Login", session['name'],session['name'], request.remote_addr)
			session['level'] = data[2]
			session['place'] = data[3]
			session['logged'] = 1
			session['name'] = data[0]
			session['work'] = data[4]

			#print(data[2], "hello")
			return redirect(url_for('main'))
		else:
			return 'wrong'
	return send_file('templates/login.html')

@app.route('/main')
def main():
	if session.get('logged') == 1:
		place = session.get('place')
		#print(session.get('name'))
		level = session.get('level')
		if level == 0:
			place = "Manager"
		else:
			place = places[place]
		return render_template("main.html", loggedin = session.get('name'), level = level, loc = place)
	else:
		return redirect(url_for('login'))


@app.route("/remove", methods=['POST', 'GET'])
def remove():
	shop_name = ''
	work = session.get('work')
	if session.get('logged') == 1:
		level = session.get('level')
		if request.method == 'POST':
			#print(request.form)
			quantity = request.form['quantity']
			item = request.form['item']
			shop = session.get('place')
			if level == 1:
				work = int(request.form['inv-type'])
			print("remove these ", item, quantity, places[shop], ttype[work])
			keeplog(' '.join(("remove these ", item, quantity, places[shop], ttype[work])), session['name'], request.remote_addr)
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
		
		if level == 0:
			return render_template('remove_manager.html')
		elif level == 1:
			return render_template('remove_sub.html')
		shop_name = places[place]
		session['place'] = place
		return render_template('remove.html', shop=shop_name+' '+work_type[work])
		
	else:
		return redirect(url_for('login'))

@app.route('/remove_manager', methods=['POST', 'GET'])
def remove_manager():
	if session.get('level') != 0:
		return redirect(url_for('remove'))

	if session.get('logged') == 1:
		if request.method == 'POST':
			#print(request.form)
			quantity = request.form['quantity']
			item = request.form['item']
			shop = request.form['shop']
			intype = request.form['inv-type']
			print("remove these ", item, quantity, shop, intype)
			keeplog(' '.join(("remove these ", item, quantity, shop, intype)), session['name'], request.remote_addr)
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
	if session.get('level') != 0:
		return redirect(url_for('add'))

	if session.get('logged') == 1:
		if request.method == 'POST':
			#print(request.form)
			#print("yess")
			quantity = request.form['quantity']
			item = request.form['item']
			shop = request.form['shop']
			intype = request.form['inv-type']
			print("add these ", item, quantity, shop, intype)
			keeplog(' '.join(("add these ", item, quantity, shop, intype)), session['name'], request.remote_addr)
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
	work = session.get('work')
	if session.get('logged') == 1:
		level = session.get('level')
		if request.method == 'POST':
			#print(request.form)
			quantity = request.form['quantity']
			item = request.form['item']
			shop = session.get('place')
			if level == 1:
				work = int(request.form['inv-type'])
				#print(work)
			print("add these ", item, quantity, places[shop], ttype[work])
			keeplog(' '.join(("add these ", item, quantity, places[shop], ttype[work])), session['name'], request.remote_addr)
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
		
		if level == 0:
			return render_template('add_manager.html')
		elif level == 1:
			return render_template('add_sub.html')
		shop_name = places[place]
		session['place'] = place
		return render_template('add.html', shop=shop_name+' '+work_type[work])
		
	else:
		return redirect(url_for('login'))

tplace = ['manial', 'gezera', 'tamooh']
ttype = ['alum', 'acc', 'fiber']

@app.route('/view', methods=['POST', 'GET'])
def view():
	choice = session.get('place')
	if session.get('logged') != 1:
		return redirect(url_for('login'))
	if session.get('level') == 0:
		if request.method == 'POST':
			#print(request.form)
			choice = request.form['shop']
			inv_type = request.form['inv-type']
			session['target'] = choice
			#print(choice, "pressed")
			table_name = '%s_%s'%(inv_type, choice)

			con = sqlite3.connect('inventory.db')
			curs = con.cursor()
			curs.execute("select * from %s;"%(table_name))
			data = curs.fetchall()
			con.close()
			return render_template("view.html", data=data, shop_name = choice + ' ' + inv_type)

		else:
			return render_template('view.html', data='')


	elif session.get('level') == 1:
		if request.method == 'POST':
			print(request.form['inv-type'])
			table_name = '%s_%s'%(ttype[int(request.form['inv-type'])-1], tplace[session.get('place')])
			con = sqlite3.connect('inventory.db')
			curs = con.cursor()
			curs.execute("select * from %s;"%(table_name))
			data = curs.fetchall()
			con.close()
			#print(session.get('place'))
			return render_template("view_sub.html", data=data, shop_name = places[choice])
		else:
			return render_template("view_sub.html", data='', shop_name = places[choice])

	elif session.get('level') == 2:
		place = tplace[session.get('place')]
		work = ttype[session.get('work')]

		table_name = '%s_%s'%(work, place)
		con = sqlite3.connect('inventory.db')
		curs = con.cursor()
		curs.execute("select * from %s;"%(table_name))
		data = curs.fetchall()
		con.close()
		return render_template("viewL.html", data=data, shop_name=places[choice])

	else:
		return "You are not authorized"


#def calc(item, quan, warhouse, inv-type, bs):


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('../certificate.pem', '../private_key.pem')
s = input("SSL Enable (1 for yes, 2 for no): ")
if s == '1':
	app.run(host='192.168.1.57', port=443, ssl_context=context)
elif s == '2':
	app.run(host='192.168.1.57', port=80)


