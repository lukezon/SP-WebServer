import web
import sqlite3

#Site Setup
urls = (
  '/', 'index', '/sqladd', 'sqladd','/sqlreq', 'sqlreq', '/sqldel', 'sqldel', "/killapp", "killapp"
)
app = web.application(urls, globals())
render = web.template.render('templates/')

#Sets up SQL database in RAM
sqlconn = sqlite3.connect(':memory:', check_same_thread=False)
c = sqlconn.cursor()
c.execute("""CREATE TABLE controlvalues (
            iot_id integer NOT NULL PRIMARY KEY,
            command_data blob)""")
sqlconn.commit()

#SQL functions Setup
def SQL_add(ID, commands):
	try:
		commands = str(commands)
		data = (ID, commands)
		c.execute("INSERT INTO controlvalues (iot_id, command_data) VALUES (?, ?)", data)
		pass
	except:
		print "error occured"
		#create some sort of overflow system here
		pass 

def SQL_req(iot_id):
	try:
		c.execute("SELECT * FROM controlvalues WHERE iot_id = ?", (iot_id))
		data = str(c.fetchall())
		return data
	except:
		return None

def SQL_del(iot_id):
	try:
		c.execute("DELETE FROM controlvalues WHERE iot_id = ?", (iot_id))
		pass
	except:
		pass


#Webpages
class index(object):
	def GET(self):
		return render.index()


class sqladd(object):
	def GET(self):
		form = web.input(iot_id=None,commands=None)
		if form.iot_id and form.commands:
			#defines variables to be used from webform
			iot_id = str(form.iot_id)
			commands = str(form.commands)
			SQL_add(iot_id, commands)
			c.execute("SELECT * FROM controlvalues")
			tablereturn = str(c.fetchall())
			return render.sqladd(error = None, iot_id = iot_id, commands = commands, tablereturn = tablereturn)
		else:
			return render.sqladd(error = "yes", iot_id = None, commands = None, tablereturn = None)

class sqlreq(object):
	def GET(self):
		form = web.input(iot_id = None, delete = False)
		if form.iot_id:
			SQL_data_return = SQL_req(str(form.iot_id))
			if form.delete == "True":
				SQL_del(str(form.iot_id))
			return SQL_data_return
		else:
			return "please provide an IOT_id number to complete your request"

class sqldel(object):
	def GET(self):
		form = web.input(iot_id = None)
		if form.iot_id:
			SQL_del(str(form.iot_id))
			return ""
		else:
			return "please input IOT_id ex: /sqladd?iot_id=2&commands=hello223"



class killapp(object):
    def GET(self):
        raise SystemExit
        return "If you are seeing this the Kill Trigger did not work!  Try manually killing the python proccess from SSH."


if __name__ == "__main__":
    app.run()