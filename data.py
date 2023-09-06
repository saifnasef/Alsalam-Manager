import sqlite3
import bcrypt
import random
import string
counter = 1
table = ''
sh = ['gezera', 'tamooh', 'manial']
intype = ['acc', 'fiber', 'alum']
data = input("1) inventory\n2) User\n3) fill inventory\nChoose: ")
if data == '1':
	con = sqlite3.connect('inventory.db')
	shop = input("1) manial\n2) gezera\n3) tamooh\nChoose: ")
	typ = input("1) alum,\n2) acc\n3) fiber\nChoose: ")
	
elif data == '3':
	con = sqlite3.connect('inventory.db')
	for i in sh:
		for j in intype:
			table = "%s_%s"%(j, i)
			for k in range(3):
				random_name = ''.join(random.choice(string.ascii_letters) for _ in range(3))
				fed = (random_name, random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))
				temp = 'insert into %s values %s;'%(table, tuple(fed))
				#print(temp)
				cursor = con.cursor()
				cursor.execute(temp)
				con.commit()
				print('done %d'%counter)
				counter +=1
	con.close()
	exit()
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
con.close()

