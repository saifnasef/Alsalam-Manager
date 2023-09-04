import sqlite3
import bcrypt
table = ''

data = input("1) inventory\n2) User\nchoose: ")
if data == '1':
	con = sqlite3.connect('inventory.db')
	table = input("1) manial\n2) gezera\n3) tamooh\nChoose: ")
	if table == '1':
		table = "alum_manial"
	elif table == '2':
		table = "alum_gezera"
	elif table == '3':
		table = "alum_tamooh"
elif data == '2':
	con = sqlite3.connect('users.db')
	table = "user"
else:
	exit("Invalid input")


cursor = con.cursor()
cursor.execute("pragma table_info(%s);"%(table))
out = cursor.fetchall()
for i in out:
	print(i)

new = input("Data to insert (separated by commas): ").split(', ')
if data == '2':
	temp = new[2].encode('utf-8')
	temp = bcrypt.hashpw(temp, bcrypt.gensalt())
	new[2] = str(temp.decode())

if len(new) == len(out):
	add = 'insert into %s values %s;'%(table, tuple(new))
	cursor.execute(add)
	con.commit()
	print(add)


