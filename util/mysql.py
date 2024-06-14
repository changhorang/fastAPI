import mysql.connector
import sys

class MySQL(object):
	def __init__(self, dbhost, dbuser, dbpass, dbname, debug=False):
		''' Intialize a Database object and connect to the database '''
		self.host = dbhost
		self.name = dbname
		self.debug = debug
		self.conn = None
		# Try to connect to the database, and if there were any errors report and quit
		try:
			self.conn = self.get_connector(dbuser, dbpass)
		except mysql.connector.Error as err:
			print(str(err))
			print('Error connecting to the host.')
			sys.exit(1)
		if self.debug:
			print('Connected to host.')
		# Get the cursor
		self.cursor = self.conn.cursor()

	def get_connector(self, username, dbpass):
		''' Connect to the database and return the connector '''
		if self.debug:
			print('Connecting to database...')
		# If there is an active connection ,return it
		if isinstance(self.conn, mysql.connector.connection.MySQLConnection):
			if self.debug:
				print('Already connected!')
			return self.conn
		return mysql.connector.connect(user = username, password = dbpass, host = self.host, database = self.name)

	def close_connection(self):
		''' Close the connection '''
		self.conn.close()
		if self.debug:
			print('Connection closed.')

	def clear_cursor(self):
		''' Clear the cursor if we don't need results (used in get_columns) '''
		if self.debug:
			print('Clearing cursor...')
		self.cursor.fetchall()

	def commit(self):
		''' Commit changes to the remote DB '''
		if self.debug:
			print('Commiting changes...')
		self.conn.commit()

	def rollback(self):
		''' Rollback changes in case of errors of any kind '''
		if self.debug:
			print('Rolling back...')
		self.conn.rollback()

	def insert(self, table, columns, values):
		''' Insert a new entry into a table with given values '''
		# Get the columns's names
		columns = str(tuple([str(x) for x in columns]))
		# Create the query statment
		query = 'INSERT INTO %s %s' % (table, columns.replace("'", ''))
		values_query = 'VALUES (' + ('%s, ' * len(values))[:-2] + ')'
		query_stmt = ' '.join([
			query,
			values_query
		])
		try:
			self.cursor.execute(query_stmt, values)
			# Commit the changes to the remote DB
			self.commit()
		except Exception as e:
			if self.debug:
				print('Error: %s' % str(e))
			# Rollback the changes from the current transaction
			self.rollback()
			raise ValueError("Can't add entry, please try again (maybe with different values?)")

	def search(self, table, column, value, partial=False, case_sensetive=True):
		''' Search for value in table '''
		select_stmt = 'SELECT * FROM %s WHERE' % str(table)
		# If we want that partial match will suffice
		if partial:
			sql_function = 'LIKE'
			value = '%%%s%%' % str(value)
		else:
			sql_function = '='
		# If we want the search to be case sensetive
		if case_sensetive:
			condition = '''`%s` %s "%s"''' % (str(column), sql_function, str(value))
		else:
			condition = '''LOWER(`%s`) %s LOWER("%s")''' % (str(column), sql_function, str(value))
		# Build to query from it's parts
		query = ' '.join([select_stmt, condition])
		query = query.replace("'", '')
		return self.__iter_results(query, 'search')

	def __del__(self):
		''' Called upon object deletion, make sure the connection to the DB is closed '''
		if self.conn is not None:
			self.close_connection()

if __name__ == '__main__':
	
	mysql = MySQL(dbhost='127.0.0.1', dbname='api_db', dbpass=1234, dbuser='root')
	mysql.get_connector()