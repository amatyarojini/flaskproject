from flask import Flask,session,redirect,request,render_template
from  random import randint
import datetime
from datetime import date
app = Flask(__name__)
app.secret_key = 'somesecrets!!'
@app.route('/')
def index():
 if not ('earned' in session and 'log' in session):
  session['earned']=0
  session['log']=[]
  print(session['earned'])
 return render_template("index.html")


@app.route('/process_money',methods=['POST'])
def process_money():
 worksite = request.form['building']

 print (worksite)
 if worksite == 'farm':
  print ("inside farm")
  gain = randint(10,20)
  print (gain)

 elif worksite == 'cave':
  print ("inside cave")
  gain = randint(5,10)
  print (gain)

 elif worksite == 'house':
  print ("inside house")
  gain = randint(2,5)
  print (gain)

 else:
  gain = randint(-50,50)
  print ("inside casino")
  print (gain)

 session['earned'] += gain

 if worksite == "casino":
  session['log'].append("Entered a casino and "+ ("earned" if gain >= 0  else "lost") + str(gain) + "golds..." + ("Yay !!" if gain >= 0  else "Ouch..") + "("+datetime.datetime.now().strftime("%Y/%m/%d %H:%M %p")+")")

 else:
  session['log'].append("Earned" + str(gain) + "golds from the " + worksite + "! ("+datetime.datetime.now().strftime("%Y/%m/%d %H:%M %p")+")")

 return redirect('/')

app.run(debug=True)
