from flask import render_template, redirect, request, session
from logic.tasksLogic import TaskLogic
import requests


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

            print("Redirected", username, "to peak tasks.", sep=" ")
            return render_template("todolist.html", userid=userid, username=username, tasks=dateTasks)

        