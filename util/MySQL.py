import mysql.connector

# from util.logWriter import logWriter

class MySQL():
	def __init__(self):
		self.host = None
		self.user = None
		self.passwd = None
		self.database = None
		self.conn = None
		self.bdVal = dict

	def connect(self, host, database, user, passwd):
		try:
			self.conn = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
			# logWriter.log.info("MySQL is Connected")
		except Exception as e:
			print(1)
			# logWriter.log.error("Connection ERROR")
		return self.conn

	def addBind(self, key, value):
		self.bdVal[key] = value

	def bdValClear(self):
		self.bdVal.clear()
  
	def rollback(self):
		self.conn.rollback()

	def commit(self):
		self.conn.commit()

	def select(self, query, bdVal=None):
		res = []
		_cursor = self.conn.cursor(dictionary=True)
		if bdVal is None:
			_cursor.execute(query, bdVal)
		else:
			_cursor.execute(query, self.bdVal)
		
		for i in _cursor:
			res.append(i)
		return res
	
	def execute(self, query, bdVal=None):
		_cursor = self.conn.cursor(dictionary=True)
		
		if bdVal is None:
			_cursor.execute(query, bdVal)
		else:
			_cursor.execute(query, self.bdVal)
		
		self.commit()
 
	def close(self):
		if self.conn is not None:
			self.conn.close()

if __name__ == '__main__':
	dbImpl = MySQL()
	dbImpl.connect(host='127.0.0.1', user='root', passwd='1234', database='api_db')
	selTest = """SELECT * FROM jwt_login"""
	res = dbImpl.select(selTest)
	print(res)
	dbImpl.close()
	