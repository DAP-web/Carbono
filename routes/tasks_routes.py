from flask import render_template, redirect, request, session
from logic.tasksLogic import TaskLogic
import requests
import random


class TasksRoutes:
    @staticmethod
    def configure_routes(app):
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

                dataJson = []
                # Recovering tip from API
                tipsIDs = []
                restapi = "https://apicarbono.herokuapp.com"
                endpoint = "/contenido"
                categoriasapi = ["/Libro", "/Consejos", "/Charla"]
                categoriaapi = random.choice(categoriasapi)

                url = f"{restapi}{endpoint}{categoriaapi}"

                response = requests.get(url)
                print(response)
                if response.status_code == 200:
                    dataJson = response.json()

                for tip in dataJson:
                    tipsIDs.append(tip["id"])

                randomtipid = random.choice(tipsIDs)
                randomtip = {}

                for tip in dataJson:
                    if int(tip["id"]) == randomtipid:
                        randomtip = tip

                print("Escogido", randomtip, sep="||")

                # Recovering trainer from API
                trainerIDs = []
                restapi = "https://apicarbono.herokuapp.com"
                endpoint = "/trainers"
                categoriasapi = ["/Efectividad", "/Liderazgo",
                                 "/Organizacion", "/Productividad"]
                categoriaapi = random.choice(categoriasapi)

                url = f"{restapi}{endpoint}{categoriaapi}"

                response = requests.get(url)
                print(response)
                if response.status_code == 200:
                    dataJson = response.json()

                for trainer in dataJson:
                    trainerIDs.append(trainer["id"])

                randomtrainerid = random.choice(trainerIDs)
                randomtrainer = {}

                for trainer in dataJson:
                    if int(trainer["id"]) == randomtrainerid:
                        randomtrainer = trainer

                print("Escogido", randomtrainer, sep="||")

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
                                           tasks=dateTasks, date=date, categorias=categorias,
                                           recomendacion=randomtip, trainer=randomtrainer)
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
                                           tasksC=dateTasksC, tasksA=dateTasksA, date=date, categorias=categorias,
                                           recomendacion=randomtip, trainer=randomtrainer)

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

                rows = logic.insertTask(
                    userid, date, task, priority, 0, categoria)
                print(f"Rows affected: {rows}", "Task for", username, "added")

                if rows > 1:
                    session["addedTask"] = "Tu tarea se ha registrado con exito."
                else:
                    session["addedTask"] = ""

                return redirect('addtask')

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
                    return redirect("peakTasks")

                elif request.form.get("delete", False):
                    for currentID in selectedIDs:
                        rows = logic.deleteTask(currentID)
                        rowsTotal += rows

                    print("Rows affected:", rowsTotal, sep=" ")
                    return redirect("peakTasks")
                else:
                    print("Estoy aqui maje")
                    return redirect('peakTasks')
            else:
                return redirect('peakTasks')
