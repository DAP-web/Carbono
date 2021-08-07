from flask import render_template, redirect, request, session
from logic.tasksLogic import TaskLogic
from logic.userLogic import UserLogic
import random
import requests


class DashboardRoutes:
    @staticmethod
    def configure_routes(app):
        @app.route("/dashboard")
        def dashboard():
            if int(session.get("login_user_CA")) == 0:
                return redirect("todolist")
            if session.get("loggedIn"):
                logic = TaskLogic()
                print("Found a session!")
                userid = session.get("login_user_id")

                username = session.get("login_user_name")
                print("Redirecting", username, userid, "to ToDoList", sep=" ")

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

                return render_template("dashboardToDo.html", userid=userid, username=username,
                                       recomendacion=randomtip, trainer=randomtrainer)
            else:
                print("Didn't find a session. Redirecting to Login!")
                return redirect("login")

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

            print("Redirecting", username, userid,
                  "to users dashboard", sep=" ")
            return render_template("dashboardUsers.html", userid=userid, username=username, users=users)

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
