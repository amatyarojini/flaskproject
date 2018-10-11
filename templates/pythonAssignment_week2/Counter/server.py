from flask import Flask,session,render_template
app = Flask(__name__)
app.secret_key = 'somesecretvalue'

@app.route("/")
def index():
 if 'counter' not in session:
  session['counter'] = 0
 session['counter'] +=1
 return render_template('index.html')

app.run(debug=True)
