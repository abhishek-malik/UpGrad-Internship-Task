#Since longin view was not mentioned in the problem statement it is not included.
#For any queries, contact developer - maps.abhishek@gmail.com
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from products import Product
import sqlite3

app = Flask(__name__)
app.secret_key = "mykey"

app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465 ,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = 'Your Mail',
    MAIL_PASSWORD = 'Your Password'
) #Please note you need to turn on the less secure apps on, on your gamil in order to send main through flask.
mail = Mail(app)


@app.route('/product-list/<product_id>', methods=['GET','POST'])
def if_interested(product_id):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	product_id = c.execute('select * from products where product_id = ?',(product_id,))
	product_id = c.fetchone()[0]
	product_name = c.execute('select * from products where product_id = ?',(product_id,))
	product_name = c.fetchone()[1]
	product_details = c.execute('select * from products where product_id = ?',(product_id,))
	product_details = c.fetchone()[2]
	if request.method == 'POST':
		name = request.form['customer_name']
		email = request.form['customer_email']
		comment = request.form['customer_comments']

		msg = Message("New Product Request",
	                  sender=email,
	                  recipients=["abhishek.malik2015@vit.ac.in"])
		msg.body = str(product_id)+" "+str(product_name)+" "+str(product_details)+" By:"+name+" Comments:"+comment
		mail.send(msg)
		flash("Mail Sent")
	elif request.method == 'GET':
		return render_template("myproduct.html", product_id=str(product_id), product_name=str(product_name), product_details=str(product_details))	 
	return render_template("myproduct.html", product_id=str(product_id), product_name=str(product_name), product_details=str(product_details))

#Function below is a custom search function and can be modified as per the need 
@app.route('/product-list', methods=["GET","POST"])
def product_list():
	product_id, product_name, product_details = Product.from_db()
	if request.method == 'GET':
		return render_template("product-list.html", data=zip(product_id,product_name,product_details))

	elif request.method == 'POST':
		keyword = request.form['keyword']
		ans = keyword
		a = []
		b = []
		c = []
		count = 0
		num = 1
		for i1, j1, k1 in zip(product_id, product_name,product_details):
			for j in j1:
				ans1 = j
				if ans1 == ans:
					a.append(i1)
					b.append(j1)
					c.append(k1)
					count = count + 1

			check = 'aaa'
			for k in k1:
				l = k.split(' ')
				for abc in l:
					if abc == ans:
						check = j1

			if check == j1:
				for var in b:
					if var == check:
						num = 0

			if num != 0 and check == j1:
				a.append(i1)
				b.append(j1)
				c.append(k1)
				count = count + 1

		if (count > 0):
			return render_template('product-list.html', data1=zip(a, b, c), data=zip(product_id,product_name,product_details))
		else:
			return redirect(url_for('product_list'))

#View to add new products
@app.route('/new_product', methods=["GET","POST"])
def new_product():
	if request.method == 'GET':
		return render_template('new_product.html')

	elif request.method == 'POST':
		product_id = request.form['product_id']
		product_name = request.form['product_name']
		product_details = request.form['product_details']

		new_product = Product(product_id,product_name,product_details)
		new_product.save_to_db()

		return redirect(url_for('product_list'))

	return render_template('new_product.html')


@app.route('/')
def home():
	#Run this only once to initialize the database.
	'''
	conn = sqlite3.connect('database.db')
	print("Opened database successfully")

	conn.execute('CREATE TABLE products (product_id TEXT, product_name TEXT, product_details TEXT)')
	print("Table created successfully")
	conn.close()'''
	return render_template('home.html')

