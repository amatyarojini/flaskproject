from flask import Flask, redirect, render_template, request, session
from random import randint
app = Flask(__name__)
app.secret_key = "SomeSecrets"

@app.route('/')
def index():
 if "number" not in session:
  session['number'] = randint(1,100)
 print (session['number'],"This is the number")
 return render_template('index.html')

@app.route('/guess', methods=["POST"])
def numberGuess():
 guess= int(request.form['guess'])
 if guess < session['number']:
     #do something
     print ("in low if")
     session['guess'] = "low"
 elif guess > session['number']:
     #do something else
     print ("in high elif")
     session['guess'] = "high"
 else:
    #Guessed NUMBER!
    print ("in match")
    session['guess'] = "match"
 return redirect('/')

@app.route('/reset')
def newGame():
    session.clear()
    return redirect('/')

app.run(debug=True)
