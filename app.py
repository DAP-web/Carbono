from enum import IntFlag
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
            params=data
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

                if isinstance(userDict, list):
                    message = "El correo o la contraseña son incorrectos. Verifica y vuelve a probar"
                    return render_template("login.html", message=message)

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
                    message = "El correo o la contraseña son incorrectos. Verifica y vuelve a probar"
                    return render_template("login.html", message=message)
            else:
                message = "¡Algo salio mal! Vuelve a probar"
                return render_template("login.html", message=message)
        else:
            message = "¡Algo salio mal! Vuelve a probar"
            return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    if session.get("loggedIn"):
        session.pop("login_user_id")
        session.pop("login_user_email")
        session.pop("login_user_name")
        session.pop("login_user_CA")
        session.pop("loggedIn")
        if session.get("date_tasksIDs"):
            session.pop("date_tasksIDs")
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
            salt = bcrypt.gensalt(rounds=14)
            epswd = password.encode("utf-8")

            hashpswd = bcrypt.hashpw(epswd, salt)

            strSalt = salt.decode("utf-8")
            strPswd = hashpswd.decode("utf-8")
            try:
                rows = logic.insertUser(
                    username, email, strPswd, strSalt, admin)
            except:
                message = "¡Ese correo ya existe!"
                return render_template("registration.html", message=message)

            print("Rows affected:", rows, sep=" ")

            return redirect("login")
        else:
            message = "Las contraseñas no coinciden. Verifique y vuelva a intentar."
            return render_template("registration.html", message=message)


@app.route("/dashboardUsers")
def dashboardUsers():
    logic = UserLogic()
    userid = session.get("login_user_id")
    username = session.get("login_user_name")
    usersids = []

    users = logic.getUsersClients()
    if session.get("usersDash"):
        session.pop("usersDash")

    for user in users:
        usersids.append(user["userid"])

    session["usersDash"] = usersids

    print("Redirecting", username, userid, "to users dashboard", sep=" ")
    return render_template("dashboardUsers.html", userid=userid, username=username, users=users)


@app.route("/removeUser")
def removeUser():
    logic = UserLogic()
    userid = session.get("login_user_id")
    username = session.get("login_user_name")

    users = logic.getUsersClients()

    print("Redirecting", username, userid, "to remove users", sep=" ")
    return render_template("removeUser.html", userid=userid, username=username, users=users)


@app.route("/removeUserBD", methods=["GET", "POST"])
def removeUserBD():
    if request.method == "GET":
        return render_template("removeUser.html")
    elif request.method == "POST":
        logic = UserLogic()

        users = session.get("usersDash")
        iduser = 0

        for user in users:
            name = "user" + str(user)
            print(name)
            deleteUserID = request.form.get(name, False)
            print(deleteUserID)
            if deleteUserID:
                iduser = user
                break

        print(iduser)
        rows = logic.deleteUserClient(iduser)

        print("Rows affected:", rows, sep=" ")
        return redirect('dashboardUsers')


@app.route("/dashboard")
def dashboard():
    if session.get("loggedIn"):
        logic = TaskLogic()
        print("Found a session!")
        userid = session.get("login_user_id")
        username = session.get("login_user_name")
        print("Redirecting", username, userid, "to ToDoList", sep=" ")

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
    logic = TaskLogic()
    userid = session.get("login_user_id")
    username = session.get("login_user_name")
    categorias = logic.traerCategorias()

    print("Redirected", username, "to add a task.", sep=" ")
    return render_template("addtask.html", userid=userid, username=username, categorias=categorias)


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
        if request.form.get("categoria", False):
            categoria = request.form.get("categoria", False)
            categoria = categoria.capitalize()
        else:
            categoria = request.form.get("nuevaCategoria", False)
            categoria = categoria.capitalize()

        rows = logic.insertTask(userid, date, task, priority, 0, categoria)
        print(f"Rows affected: {rows}", "Task for", username, "added")

        if rows > 1:
            session["addedTask"] = "Tu tarea se ha registrado con exito."
        else:
            session["addedTask"] = ""

        return redirect('addtask')


@app.route("/todolist")
def todolist():
    if int(session.get("login_user_CA")) == 1:
        return redirect("dashboard")

    userid = session.get("login_user_id")
    username = session.get("login_user_name")

    dateTasks = []

    print("Redirected", username, "to peak tasks.", sep=" ")
    return render_template("todolist.html", userid=userid, username=username, tasks=dateTasks)


@app.route("/peakTasks", methods=["GET", "POST"])
def peakTasks():
    if request.method == "GET":
        if int(session.get("login_user_CA")) == 0:
            return redirect("todolist")
        elif int(session.get("login_user_CA")) == 1:
            return redirect("dashboard")
    elif request.method == "POST":
        userid = session.get("login_user_id")
        username = session.get("login_user_name")

        logic = TaskLogic()

        date = request.form["date"]
        month = date[0:2]
        day = date[3:5]
        year = date[6:]
        date = year + "-" + month + "-" + day
        print(date)

        if session.get("current_date"):
            session.pop("current_date")
            print("Found a previos date and removed it!")

        session["current_date"] = date

        categorias = logic.traerCategorias()

        if int(session.get("login_user_CA")) == 0:
            tasks = logic.getAllTasksByUser(userid)
            dateTasks, tasksIDs = [[], []]

            for task in tasks:
                if date == str(task["date"]):
                    dateTasks.append(task)
                    tasksIDs.append(task["taskid"])
                else:
                    continue

            if session.get("date_tasksIDs"):
                session.pop("date_tasksIDs")
                print("Found a previos list and removed it!")

            session["date_tasksIDs"] = tasksIDs

            print(dateTasks)
            return render_template("todolist.html", userid=userid, username=username,
                                   tasks=dateTasks, date=date, categorias=categorias)
        elif int(session.get("login_user_CA")) == 1:
            tasksC = logic.getAllTasksClients()
            tasksA = logic.getAllTasksByUser(userid)
            dateTasksC, dateTasksA, tasksIDs = [[], [], []]

            for task in tasksC:
                if date == str(task["date"]):
                    dateTasksC.append(task)
                    tasksIDs.append(task["taskid"])
                else:
                    continue

            for task in tasksA:
                if date == str(task["date"]):
                    dateTasksA.append(task)
                    tasksIDs.append(task["taskid"])
                else:
                    continue

            if session.get("date_tasksIDs"):
                session.pop("date_tasksIDs")
                print("Found a previos list and removed it!")

            session["date_tasksIDs"] = tasksIDs

            print(dateTasksC, dateTasksA)
            return render_template("dashboardToDo.html", userid=userid, username=username,
                                   tasksC=dateTasksC, tasksA=dateTasksA, date=date, categorias=categorias)


@app.route("/beneficios")
def beneficios():
    return render_template("beneficios.html")


@app.route("/acerca")
def acerca():
    return render_template("acerca.html")


@app.route("/contactanos")
def contactanos():
    return render_template("contactanos.html")


@app.route("/checkTask", methods=["GET", "POST"])
def checkTask():
    if request.method == "GET":
        return redirect("todolist")
    elif request.method == "POST":
        tasksIDs = session.get("date_tasksIDs")

        selectedIDs = []
        for currentID in tasksIDs:
            name = "tarea" + str(currentID)
            id = request.form.get(name, False)
            print(id)
            if id:
                selectedIDs.append(int(id))
        print(selectedIDs)

        logic = TaskLogic()
        rowsTotal = 0

        if request.form.get("update", False):
            for currentID in selectedIDs:
                rows = logic.updateTask(currentID)
                rowsTotal += rows

            print("Rows affected:", rowsTotal, sep=" ")
            return redirect("todolist")

        elif request.form.get("delete", False):
            for currentID in selectedIDs:
                rows = logic.deleteTask(currentID)
                rowsTotal += rows

            print("Rows affected:", rowsTotal, sep=" ")
            return redirect("todolist")


@app.route("/filterTasks", methods=["GET", "POST"])
def filterTasks():
    if request.method == "GET":
        return redirect("todolist")
    elif request.method == "POST":
        logic = TaskLogic()

        # Recuperando informacion sobre el usuario
        userid = session.get("login_user_id")
        username = session.get("login_user_name")

        # Pidiendo la fecha a aplicar los filtros
        date = session.get("current_date")

        categorias = logic.traerCategorias()

        # Recuperando Informacion del form
        sol_prioridad = request.form["filtroPrioridad"]
        sol_categoria = request.form["filtroCategoria"]
        sol_estado = request.form["filtroEstado"]

        # Comprobando si es Cliente o Administrador
        if int(session.get("login_user_CA")) == 0:
            tasksAll = logic.getAllTasksByUser(userid)
            tasks, filteredTasks, filteredTasksIDs = [[], [], []]
            fprior, fcat, fest = [[], [], []]

            # Verificando fecha de las tareas
            for task in tasksAll:
                if date == str(task["date"]):
                    tasks.append(task)
                else:
                    continue
            # Filtro por prioridad
            if sol_prioridad != "-":
                for task in tasks:
                    if sol_prioridad == str(task["priority"]):
                        fprior.append(task["taskid"])
                    else:
                        continue
            else:
                for task in tasks:
                    fprior.append(task["taskid"])

            # Filtro por categoria
            if sol_categoria != "-":
                for task in tasks:
                    if sol_categoria == str(task["categoria"]):
                        fcat.append(task["taskid"])
                    else:
                        continue
            else:
                for task in tasks:
                    fcat.append(task["taskid"])

            # Filtro por estado
            if sol_estado != "-":
                for task in tasks:
                    if sol_estado == str(task["estado"]):
                        fest.append(task["taskid"])
                    else:
                        continue
            else:
                for task in tasks:
                    fest.append(task["taskid"])

            # Filtrando entre listas filtradas de IDs
            for currentID in fprior:
                if currentID in fcat and currentID in fest:
                    filteredTasksIDs.append(currentID)

            # Encontrando tareas
            for task in tasks:
                if task["taskid"] in filteredTasksIDs:
                    filteredTasks.append(task)

            if session.get("date_tasksIDs"):
                session.pop("date_tasksIDs")
                print("Found a previos list and removed it!")

            session["date_tasksIDs"] = filteredTasksIDs

            print(filteredTasks)
            return render_template("todolist.html", userid=userid, username=username,
                                   tasks=tasks, date=date, categorias=categorias)

        elif int(session.get("login_user_CA")) == 1:
            tasksCAll = logic.getAllTasksClients()
            tasksAAll = logic.getAllTasksByUser(userid)
            tasksC, tasksA = [[], []]
            filteredTasksC, filteredTasksA, filteredTasksIDs = [[], [], []]
            fpriorC, fcatC, festC = [[], [], []]
            fpriorA, fcatA, festA = [[], [], []]

            # Verificando fecha de las tareas
            for task in tasksCAll:
                if date == str(task["date"]):
                    tasksC.append(task)
                else:
                    continue

            for task in tasksAAll:
                if date == str(task["date"]):
                    tasksA.append(task)
                else:
                    continue

            # Filtro por prioridad
            if sol_prioridad != "-":
                for task in tasksC:
                    if sol_prioridad == str(task["priority"]):
                        fpriorC.append(task["taskid"])
                    else:
                        continue

                for task in tasksA:
                    if sol_prioridad == str(task["priority"]):
                        fpriorA.append(task["taskid"])
                    else:
                        continue
            else:
                for task in tasksC:
                    fpriorC.append(task["taskid"])

                for task in tasksA:
                    fpriorA.append(task["taskid"])

            # Filtro por categoria
            if sol_categoria != "-":
                for task in tasksC:
                    if sol_categoria == str(task["categoria"]):
                        fcatC.append(task["taskid"])
                    else:
                        continue

                for task in tasksA:
                    if sol_categoria == str(task["categoria"]):
                        fcatA.append(task["taskid"])
                    else:
                        continue
            else:
                for task in tasksC:
                    fcatC.append(task["taskid"])

                for task in tasksA:
                    fcatA.append(task["taskid"])

            # Filtro por estado
            if sol_estado != "-":
                for task in tasksC:
                    if sol_estado == str(task["estado"]):
                        festC.append(task["taskid"])
                    else:
                        continue

                for task in tasksA:
                    if sol_estado == str(task["estado"]):
                        festA.append(task["taskid"])
                    else:
                        continue
            else:
                for task in tasksC:
                    festC.append(task["taskid"])

                for task in tasksA:
                    festA.append(task["taskid"])

            # Filtrando entre listas filtradas de IDs
            for currentID in fpriorC:
                if currentID in fcatC and currentID in festC:
                    filteredTasksIDs.append(currentID)

            for currentID in fpriorA:
                if currentID in fcatA and currentID in festA:
                    filteredTasksIDs.append(currentID)

            # Encontrando tareas
            for task in tasksC:
                if task["taskid"] in filteredTasksIDs:
                    filteredTasksC.append(task)

            for task in tasksA:
                if task["taskid"] in filteredTasksIDs:
                    filteredTasksA.append(task)

            if session.get("date_tasksIDs"):
                session.pop("date_tasksIDs")
                print("Found a previos list and removed it!")

            session["date_tasksIDs"] = filteredTasksIDs

            print(filteredTasksC, filteredTasksA, sep="|**|")
            return render_template("dashboardToDo.html", userid=userid, username=username,
                                   tasksC=filteredTasksC, tasksA=filteredTasksA, date=date,
                                   categorias=categorias)


if __name__ == "__main__":
    app.run(debug=True)
