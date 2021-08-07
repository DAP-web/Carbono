from flask import render_template, redirect, request, session
from logic.tasksLogic import TaskLogic
import random
import requests


class FilterRoutes:
    @staticmethod
    def configure_routes(app):
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
                print(date)

                categorias = logic.traerCategorias()

                # Recuperando Informacion del form
                sol_prioridad = request.form["filtroPrioridad"]
                sol_categoria = request.form["filtroCategoria"]
                sol_estado = request.form["filtroEstado"]

                print(sol_prioridad, sol_categoria, sol_estado)

                dataJson = []
                # Recovering tip from API
                messageAPIFailure_tip = ""
                tipsIDs = []
                randomtip = {}
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

                    for tip in dataJson:
                        if int(tip["id"]) == randomtipid:
                            randomtip = tip

                    print("Escogido", randomtip, sep="||")

                else:
                    messageAPIFailure_tip = "No hay recomendación por el momento. Recarga la página si deseas volver a probar."

                # Recovering trainer from API
                trainerIDs = []
                randomtrainer = {}
                messageAPIFailure_trainer = ""
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
                    

                    for trainer in dataJson:
                        if int(trainer["id"]) == randomtrainerid:
                            randomtrainer = trainer

                    print("Escogido", randomtrainer, sep="||")
                else:
                    messageAPIFailure_trainer = "No hay trainer por el momento. Recarga la página si deseas volver a probar."


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
                    print(filteredTasksIDs)

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
                                           tasks=filteredTasks, date=date, categorias=categorias,
                                           recomendacion=randomtip, trainer=randomtrainer,
                                           failTip = messageAPIFailure_tip, failTrainer = messageAPIFailure_trainer)

                elif int(session.get("login_user_CA")) == 1:
                    tasksCAll = logic.getAllTasksClients()
                    tasksAAll = logic.getAllTasksByUser(userid)
                    tasksC, tasksA = [[], []]
                    filteredTasksC, filteredTasksA, filteredTasksIDs = [
                        [], [], []]
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
                                           categorias=categorias, recomendacion=randomtip, trainer=randomtrainer,
                                           failTip = messageAPIFailure_tip, failTrainer = messageAPIFailure_trainer)
