from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS, cross_origin
import bcrypt
import requests
from logic.userLogic import UserLogic
from logic.tasksLogic import TaskLogic

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.secret_key = "B4DB7NN7B4B7"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        """validaciones de recaptha y base de datos"""
        data = {
            "secret": "6LdRpTIbAAAAANFNF3qMLkGENIHmwPHORK_nY2Dw",
            "response": request.form["g-recaptcha-response"]
        }

        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            params = data
        )

        if response.status_code == 200:
            messageJson = response.json()
            print(messageJson)

            if messageJson["success"]:
                """VALIDACIÓN"""
                logic = UserLogic()
                email = request.form["email"]
                passwd = request.form["passw"]
                userDict = logic.getUserByEmail(email)
                salt = userDict["salt"].encode("utf-8")
                hashPasswd = bcrypt.hashpw(passwd.encode("utf-8"), salt)
                dbPasswd = userDict["password"].encode("utf-8")
                if hashPasswd == dbPasswd:
                    """SESIÓN"""
                    session["login_user_id"] = userDict["userid"]
                    session["login_user_email"] = email
                    session["login_user_name"] = userDict["username"]
                    session["login_user_CA"] = userDict["admin"]
                    session["loggedIn"] = True
                    print(userDict["admin"])
                    if userDict["admin"] == 0:
                        print("cliente -> calendar")
                        return redirect("todolist")
                    elif userDict["admin"] == 1:
                        print("admin -> dashboard")
                        return redirect("dashboard")
                    else:
                        print("Algo anda mal papi!")
                        return redirect("dashboard")
                else:
                    return redirect("login")
            else:
                return redirect("login")
        else:
            return redirect("login")

@app.route("/logout")
def logout():
    if session.get("loggedIn"):
        session.pop("login_user_id")
        session.pop("login_user_email")
        session.pop("login_user_name")
        session.pop("login_user_CA")
        session.pop("loggedIn")
        print("Session removed!")
        return redirect("login")
    else:
        return redirect("login")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")
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
            print("Rows affected:", rows, sep = " ")

            return redirect("login")
        else:
            message = "Las contraseñas no coinciden. Verifique y vuelva a intentar."
            return redirect("registration", message = message)

@app.route("/dashboard1")
def dashboard1():
    return render_template("dashboard1.html")

@app.route("/dashboard")
def dashboard():
    if session.get("loggedIn"):
        logic = TaskLogic()
        print("Found a session!")
        userid = session.get("login_user_id")
        username = session.get("login_user_name")
        print("Redirecting", username, userid, "to ToDoList", sep = " ")
        
        return render_template("dashboardToDo.html", userid=userid, username=username)
    else:
        print("Didn't find a session. Redirecting to Login!")
        return redirect("login")

@app.route("/calendar")
def calendar():
    if session.get("loggedIn"):
        logic = TaskLogic()
        print("Found a session!")
        userid = session.get("login_user_id")
        username = session.get("login_user_name")
        
        return render_template("calendar.html", userid=userid, username=username)
    else:
        print("Didn't find a session. Redirecting to Login!")
        return redirect("login")

@app.route("/addtask")
def addtask():
    userid = session.get("login_user_id")
    username = session.get("login_user_name")

    print("Redirected", username, "to add a task.", sep=" ")
    return render_template("addtask.html", userid=userid, username=username)

@app.route("/addtaskbd", methods=["GET", "POST"])
def addtasktoBD():
    logic = TaskLogic()
    userid = session.get("login_user_id")
    username = session.get("login_user_name")
    
    if request.method == "GET":
        return redirect('addtask')
    elif request.method == "POST":
        date = request.form["date"]
        month = date[0:2]
        day = date[3:5]
        year = date[6:]
        date = year + "-" + month + "-" + day
        print(date)

        task = request.form["task"]
        priority = request.form["priority"]

        rows = logic.insertTask(userid, date, task, priority, 0)
        print(f"Rows affected: {rows}", "Task for", username, "added")
        
        if rows > 1:
            session["addedTask"] = "Tu tarea se ha registrado con exito."
        else:
            session["addedTask"] = ""

        return redirect('addtask')

@app.route("/todolist")
def todolist():
    userid = session.get("login_user_id")
    username = session.get("login_user_name")
    dateTasks = []

    print("Redirected", username, "to peak tasks.", sep=" ")
    return render_template("todolist.html", userid=userid, username=username, tasks = dateTasks)

@app.route("/peakTasks", methods=["GET", "POST"])
def peakTasks():
    if request.method == "GET":
        return redirect("todolist")
    elif request.method == "POST":
        if int(session.get("login_user_CA")) == 0:
            logic = TaskLogic()
            userid = session.get("login_user_id")
            username = session.get("login_user_name")
            tasks = logic.getAllTasksByUser(userid)
            dateTasks = []

            date = request.form["date"]
            month = date[0:2]
            day = date[3:5]
            year = date[6:]
            date = year + "-" + month + "-" + day
            print(date)

            for task in tasks:
                if date == str(task["date"]):
                    dateTasks.append(task)
                else:
                    continue
            print(dateTasks)
            return render_template("todolist.html", userid=userid, username=username, tasks=dateTasks, date = date)
        elif int(session.get("login_user_CA")) == 1:
            logic = TaskLogic()

            userid = session.get("login_user_id")
            username = session.get("login_user_name")
            ca = session.get("login_user_CA")
            tasksC = logic.getAllTasksClients()
            tasksA = logic.getAllTasksByUser(userid)
            dateTasksC = []
            dateTasksA = []

            date = request.form["date"]
            month = date[0:2]
            day = date[3:5]
            year = date[6:]
            date = year + "-" + month + "-" + day
            print(date)

            for task in tasksC:
                if date == str(task["date"]):
                    dateTasksC.append(task)
                else:
                    continue

            for task in tasksA:
                if date == str(task["date"]):
                    dateTasksA.append(task)
                else:
                    continue

            print(dateTasksC, dateTasksA)
            return render_template("dashboardToDo.html", userid=userid, username=username, tasksC=dateTasksC, tasksA = dateTasksA, date = date)
        # else:
        #     return redirect('todolist')


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
