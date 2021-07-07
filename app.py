from flask import Flask, render_template, request, redirect
from flask_cors import CORS, cross_origin
import bcrypt
from logic.userLogic import UserLogic

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        logic = UserLogic()

        username = request.form["usuario_reg"]
        email = request.form["correo_reg"]
        password = request.form["contra_reg"]
        cPassword = request.form["contraConf_reg"]
        admin = request.form["adminORClient"]

        if password == cPassword:
            salt = bcrypt.gensalt(rounds = 14)
            epswd = password.encode("utf-8")

            hashpswd = bcrypt.hashpw(epswd, salt)

            strSalt = salt.decode("utf-8")
            strPswd = hashpswd.decode("utf-8")

            rows = logic.insertUser(username, email, strPswd, strSalt, admin)

            return redirect("login")
        else:
            return redirect("register")

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
