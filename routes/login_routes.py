from flask import render_template, request, redirect, session
import requests
from logic.userLogic import UserLogic
import bcrypt


class LoginRoutes:
    @staticmethod
    def configure_routes(app):
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

                        hashPasswd = bcrypt.hashpw(
                            passwd.encode("utf-8"), salt)
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
