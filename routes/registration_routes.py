from flask import render_template, request, redirect, session
import requests
from logic.userLogic import UserLogic
import bcrypt


class RegisterRoutes:
    @staticmethod
    def configure_routes(app):
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
