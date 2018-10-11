# import Flask
from flask import Flask, render_template, redirect, request, session, flash,jsonify,send_file
from pathlib import Path,os
from mysqlconnection import MySQLConnector
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
mysql = MySQLConnector(app, '2018project')
# the "re" module will let us perform some regular expression operations
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


app.secret_key = "ThisIsSecret!"
@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")
@app.route('/process', methods=['POST'])
def submit():
    va = True
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        va = False
    # else if email doesn't match regular expression display an "invalid email address" message
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        va = False

    if len(request.form['password']) < 1:
        flash("Please enter password!")
        va = False

    elif not re.match(r'[A-Za-z0-9@#$%^&+=*()`~/,.:;|]{6,}', request.form['password']):
        flash("Passowrd must be atleast 6 characters and contain uppercase,lowercase,special characters")
        va = False
    if(va== True):
     if not(request.form['password'] == request.form['confirmpw']):
        flash("password dont match!")
     else:


        print("reached here")
        query = "INSERT INTO customers (email, password,created_at, updated_at) VALUES (:email, :password, NOW(), NOW())"
        # We'll then create a dictionary of data from the POST data received.
        data = {
                'email': request.form['email'],
                'password':  request.form['password'],
               }
         # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)
        flash("Sign up successfully!")
    return redirect('/')
@app.route('/signinpage')
def signin():
 return render_template("signin.html")

@app.route('/login', methods=['POST'])
def login():

 emailid = request.form['email']
 session['emailAdd'] = emailid
 print (session['emailAdd'])
 password = request.form['password']
 query = "SELECT COUNT(*) FROM  customers  WHERE email = :specificvalue1 and  password = :specifiedvalue2"
 data = {'specificvalue1': emailid,
         'specifiedvalue2': password  }
 count = mysql.query_db(query,data)
 print (count)
 for x in count:
  '''print (x['COUNT(*)']) '''
  val1 = x['COUNT(*)']
 print (val1)
 if val1 == 1:
  flash("You are logged in sucessfully!")
  return redirect('/mainpage')
 else:
  flash("email or password don't match!")
  return redirect('/signinpage')
  print("email or password don't match!")
 print ("reached here!!!!!")

@app.route('/mainpage')
def main():
 return render_template("mainpage.html")

@app.route('/mainpage/productType')
def displayProductType():
 return render_template("productType.html")


@app.route('/mainpage/productType/dresses',methods =['POST'])
def displayProductType1():
 pdType = request.form['pdType']
 query = "select product_name,price from products2 where product_type = :value1"
 data = {'value1': pdType}
 products = mysql.query_db(query,data)
 print (products)
 for x in products:

  p = x['product_name']
  file_name = p +'.jpg'
  print ("filename",file_name)
  fullpath = os.path.join('static\\img\\',file_name)
  print (fullpath)
  """return send_file(fullpath)"""

 return render_template("productType.html",all_products = products,fileName =file_name )

@app.route('/mainpage/productType2',methods =['POST'])
def displayProductType2():
 pdType = request.form['pdType']
 query = "select product_name,price from products2 where product_type = :value2"
 data = {'value2': pdType}
 products = mysql.query_db(query,data)
 print (products)
 return render_template("productType2.html",all_products = products)

@app.route('/mainpage/productType/dresses/addtocart',methods =['POST'])
def addToCart():
 y= 0
 z = 0;
 pdname = request.form['pdname']
 print("inside addcart...heyyyyyyyyyyyyyyyyyyyyyyyyyy>>",pdname)
 price = request.form['price']
 print("inside addcart...heyyyyyyyyyyyyyyyyyyyyyyyyyy>> item price",price)
 email = session.get('emailAdd')
 query = "select id from customers where email = :value1;"
 data = {'value1': email}
 customerId = mysql.query_db(query,data)
 for x in customerId:
  y = x['id']
 session['custId'] = y #storing value in session
 queryb = "select id from products2 where product_name = :value2;"
 datab = {'value2':pdname}
 pdId = mysql.query_db(queryb,datab)
 for x in pdId:
  z = x['id']
 queryc = "insert into customers_orders_products(amount,customerid,pdid) values(:value1,:value2,:value3)"
 datac = {'value1': price,
         'value2' : y,
         'value3' : z}
 mysql.query_db(queryc, datac)
 print (pdId)
 print (customerId)
 print ("heyyyyy meeee",session.get('emailAdd'))
 print (pdname)
 return render_template('productType.html')


@app.route('/mainpage/productType/dresses/myCart',methods =['POST'])
def showMyCart():
 email = session.get('emailAdd')
 query = "select id from customers where email = :value1;"
 data = {'value1': email}
 customerId = mysql.query_db(query,data)
 for x in customerId:
  y = x['id']

 print("custId",y)
 query = "SELECT GROUP_CONCAT(pdid SEPARATOR ', ') as a  FROM customers_orders_products where customerid = :value;"
 data = {'value':y
         }
 pdIdList = mysql.query_db(query,data)
 for x in pdIdList:
  y = x['a']
  print (y)
  mylist = [int(x) for x in y.split(',')]
  print (mylist)

  new_list = []
  for i in mylist:
   print(i)
   query = "SELECT  product_name, price FROM products2 where id = :value;"
   data = {'value':i
           }
   productdata = mysql.query_db(query,data)
   for j in productdata:
    new_list.append(j)
   print (new_list)
   sum = 0
   for a in new_list:
    sum = sum+a['price']
   print(sum)


 return render_template('myCart.html',myitems = new_list,total = sum)


@app.route('/mainpage/productType/dresses/addtocart/remove',methods =['POST'])
def  deleteItem():

 pdname = request.form['pdname']
 print("Im inside remove productname",pdname)
 query = "SELECT id  from products2 where product_name = :value;"
 data = {'value': pdname

         }
 pdId = mysql.query_db(query,data)
 for x in pdId:
  y = x['id']
 print("insdei remove",y)

 query2 = "DELETE FROM customers_orders_products where pdid = :value2;"
 data2 = {'value2':y

          }
 mysql.query_db(query2,data2)
 return render_template("myCart.html")

@app.route('/mainpage/productType/dresses/myCart/checkOut',methods =['POST'])
def  checkOut():
 totalAmount = request.form['total']
 return render_template('checkOut.html',total = totalAmount )
app.run(debug=True)
