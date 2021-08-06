from flask import render_template, redirect, request, session
from logic.tasksLogic import TaskLogic
from logic.userLogic import UserLogic


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

                return render_template("dashboardToDo.html", userid=userid, username=username)
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
