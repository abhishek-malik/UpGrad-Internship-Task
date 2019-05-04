from flask import flash, session
import sqlite3

class Product(object):
	def __init__(self, pid, pname, pdetails):
		self.pid = pid
		self.pname = pname
		self.pdetails = pdetails

	def save_to_db(self):
		conn = sqlite3.connect('database.db')
		try:
			c = conn.cursor()
			c.execute("INSERT INTO products (product_id,product_name,product_details) VALUES (?,?,?)",(self.pid,self.pname,self.pdetails))  
			conn.commit()
			msg = "Record added successfully"
			flash(msg)
			conn.close()
		except Exception as e:
			conn.rollback()
			msg = "Error in insert operation"
			flash(str(e))
			conn.close()

	@classmethod
	def from_db(cls):
		conn = sqlite3.connect('database.db')
		c = conn.cursor()
		product_id = c.execute("select product_id from products")
		product_id = c.fetchall()

		product_name = c. execute("select product_name from products")
		product_name = c.fetchall()

		product_details = c.execute("select product_details from products")
		product_details = c.fetchall()

		return product_id, product_name, product_details


