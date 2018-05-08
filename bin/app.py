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
            ir_stat integer,
            ir_values blob)""")
sqlconn.commit()

#SQL functions Setup
def SQL_add(ID = "NULL", value1 = "NULL", value2 = "NULL"):
	try:
		data = (ID, value1, value2)
		c.execute("INSERT INTO controlvalues (iot_id, ir_stat, ir_values) VALUES (?, ?, ?)", data)
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
		form = web.input(iot_id=None,ir_stat=None,ir_values=None)
		if form.iot_id and form.ir_stat and form.ir_values:
			#defines variables to be used from webform
			iot_id = str(form.iot_id)
			ir_stat = str(form.ir_stat)
			ir_values = str(form.ir_values)
			SQL_add(iot_id, ir_stat, ir_values)
			c.execute("SELECT * FROM controlvalues")
			tablereturn = str(c.fetchall())
			return render.sqladd(error = None, iot_id = iot_id, ir_stat = ir_stat, ir_values = ir_values, tablereturn = tablereturn)
		else:
			return render.sqladd(error = "yes", iot_id = None, ir_stat = None, ir_values = None, tablereturn = None)

class sqlreq(object):
	def GET(self):
		form = web.input(iot_id = None)
		if form.iot_id:
			return SQL_req(str(form.iot_id))
		else:
			return "please provide an IOT_id number to complete your request"

class sqldel(object):
	def GET(self):
		form = web.input(iot_id = None)
		if form.iot_id:
			SQL_del(str(form.iot_id))
			return ""
		else:
			return "please input IOT_id ex: /sqladd?iot_id=2&ir_stat=1&ir_values=hello223"






class killapp(object):
    def GET(self):
        raise SystemExit
        return "If you are seeing this the Kill Trigger did not work!  Try manually killing the python proccess from SSH."


if __name__ == "__main__":
    app.run()