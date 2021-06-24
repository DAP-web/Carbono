from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    print('whatthehell')
    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    return render_template("registration.html")

@app.route("/dashboard1")
def dashboard1():
    return render_template("dashboard1.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/todolist")
def todolist():
    return render_template("todolist.html")

@app.route("/beneficios")
def beneficios():
    return render_template("beneficios.html")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route("/contactanos")
def contactanos():
    return render_template("contactanos.html")

if __name__ == "__main__":
    app.run(debug=True)
