from flask import render_template, redirect, request, session
from logic.tasksLogic import TaskLogic
import requests
import random


class CalendarRoutes:
    @staticmethod
    def configure_routes(app):
        @app.route("/todolist")
        def todolist():
            if int(session.get("login_user_CA")) == 1:
                return redirect("dashboard")

            userid = session.get("login_user_id")
            username = session.get("login_user_name")
            dateTasks = []

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

            print("Redirected", username, "to peak tasks.", sep=" ")
            return render_template("todolist.html", userid=userid, username=username,
                                   tasks=dateTasks, recomendacion=randomtip, trainer=randomtrainer)
