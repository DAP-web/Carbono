# from enum import IntFlag
from flask import Flask  # , render_template, request, redirect, session
from flask_cors import CORS, cross_origin
# import bcrypt
# import requests
# from logic.userLogic import UserLogic
# from logic.tasksLogic import TaskLogic
from routes.main_routes import MainRoutes
from routes.login_routes import LoginRoutes
from routes.registration_routes import RegisterRoutes
from routes.calendar_routes import CalendarRoutes
from routes.dashboard_routes import DashboardRoutes
from routes.filter_routes import FilterRoutes
from routes.tasks_routes import TasksRoutes

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.secret_key = "B4DB7NN7B4B7"

MainRoutes.configure_routes(app)
LoginRoutes.configure_routes(app)
RegisterRoutes.configure_routes(app)
CalendarRoutes.configure_routes(app)
DashboardRoutes.configure_routes(app)
FilterRoutes.configure_routes(app)
TasksRoutes.configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
